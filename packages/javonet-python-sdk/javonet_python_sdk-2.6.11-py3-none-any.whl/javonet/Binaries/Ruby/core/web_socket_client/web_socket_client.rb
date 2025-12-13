require 'uri'
require 'socket'
require 'openssl'
require 'websocket'

class WebSocketClient
  class << self
    def add_or_get_client(url)
      cache[url] && cache[url].open? ? cache[url] : (cache[url]&.close; cache[url] = new(url))
    end

    def send_message(url, message)
      client = add_or_get_client(url)
      client.send_message(message)
      return client.receive_message
    rescue Errno::EPIPE, Errno::ECONNRESET, Errno::ETIMEDOUT, IOError, SystemCallError
      # Socket likely died due to server idle-timeout; rebuild without sending CLOSE
      close_client(url, suppress_close_frame: true)
      client = add_or_get_client(url)
      client.send_message(message)
      client.receive_message
    end

    def close_client(url, suppress_close_frame: false)
      cache[url]&.close(suppress_close_frame: suppress_close_frame)
      cache.delete(url)
    end

    # Returns :OPEN, :CLOSED, or nil (no client)
    def get_state(url)
      c = cache[url]
      return nil unless c
      c.open? ? :OPEN : :CLOSED
    end

    private

    def cache
      @cache ||= {}
    end
  end

  def initialize(url)
    @uri = URI.parse(url)
    raise "Only ws:// or wss:// URLs are supported" unless %w[ws wss].include?(@uri.scheme)

    @host = @uri.host
    @port = @uri.port || default_port
    @path = (@uri.path.nil? || @uri.path.empty?) ? '/' : @uri.path
    @path += "?#{@uri.query}" if @uri.query

    @socket = open_socket
    @handshake = WebSocket::Handshake::Client.new(url: url) # masks handled by client frames
    perform_handshake
    @incoming = WebSocket::Frame::Incoming::Client.new(version: @handshake.version)
  end

  # message can be an Array<Integer 0..255> or a String of bytes
  def send_message(message)
    data =
      case message
      when String then message.b
      when Array  then message.pack('C*')
      else raise ArgumentError, "Unsupported message type: #{message.class}"
      end

    frame = WebSocket::Frame::Outgoing::Client.new(
      version: @handshake.version,
      data: data,
      type: :binary
    )
    write_all(frame.to_s)
    true
  end

  # Returns Array<Integer> (bytes) or nil on timeout
  def receive_message(timeout: 5)
    deadline = Time.now + timeout
    payload_chunks = []

    loop do
      # try to parse any buffered data first
      if (frame = @incoming.next)
        case frame.type
        when :binary, :text, :continuation
          payload_chunks << frame.data
          return payload_chunks.join.bytes
        when :ping
          send_pong(frame.data)
        when :close
          send_close_reply
          return nil
        end
        next
      end

      # no complete frame yet—read from socket or timeout
      remaining = deadline - Time.now
      return nil if remaining <= 0

      if IO.select([@socket], nil, nil, [remaining, 0.05].max)
        begin
          chunk = @socket.read_nonblock(64 * 1024, exception: false)
          case chunk
          when nil
            # peer closed
            return nil
          when :wait_readable
            next
          else
            @incoming << chunk
          end
        rescue IO::WaitReadable
          next
        rescue EOFError
          return nil
        end
      end
    end
  end

  def open?
    return false if @socket.closed?
    true
  rescue IOError, SystemCallError
    false
  end

  def close(suppress_close_frame: false)
    begin
      send_close_reply unless suppress_close_frame || @socket.closed?
    rescue Errno::EPIPE, Errno::ECONNRESET, IOError, SystemCallError
      # peer already gone — ignore
    ensure
      @socket.close unless @socket.closed?
    end
  end

  private

  def default_port
    @uri.scheme == 'wss' ? 443 : 80
  end

  def open_socket
    tcp = TCPSocket.new(@host, @port)
    tcp.sync = true

    return tcp unless @uri.scheme == 'wss'

    ctx = OpenSSL::SSL::SSLContext.new
    # NOTE: for production, set VERIFY_PEER and provide a store/ca_file.
    ctx.set_params(verify_mode: OpenSSL::SSL::VERIFY_NONE)

    ssl = OpenSSL::SSL::SSLSocket.new(tcp, ctx)
    ssl.sync_close = true
    ssl.hostname = @host
    ssl.connect
    ssl
  end

  def perform_handshake
    write_all(@handshake.to_s)
    # Read until the handshake object reports finished or the server closes
    loop do
      break if @handshake.finished?
      if IO.select([@socket], nil, nil, 5)
        begin
          data = @socket.read_nonblock(4096, exception: false)
          case data
          when nil
            break
          when :wait_readable
            next
          else
            @handshake << data
          end
        rescue IO::WaitReadable
          next
        end
      else
        raise "WebSocket handshake timeout"
      end
    end

    raise "WebSocket handshake failed!" unless @handshake.finished? && @handshake.valid?
  end

  def write_all(data)
    total = 0
    while total < data.bytesize
      written = @socket.write_nonblock(data.byteslice(total..-1), exception: false)
      case written
      when :wait_writable
        IO.select(nil, [@socket])
        next
      when 0, nil
        raise IOError, "socket closed while writing"
      else
        total += written
      end
    end
  rescue IO::WaitWritable
    IO.select(nil, [@socket]); retry
  rescue Errno::EPIPE, Errno::ECONNRESET
    # bubble up for send_message to handle reconnect logic
    raise
  end

  def send_pong(data)
    pong = WebSocket::Frame::Outgoing::Client.new(
      version: @handshake.version, type: :pong, data: data
    )
    write_all(pong.to_s)
  rescue Errno::EPIPE, Errno::ECONNRESET, IOError, SystemCallError
    # ignore: socket already gone; next send will recreate
  end

  def send_close_reply
    return if @socket.closed?
    frame = WebSocket::Frame::Outgoing::Client.new(
      version: @handshake.version, type: :close
    )
    write_all(frame.to_s)
  rescue Errno::EPIPE, Errno::ECONNRESET, IOError, SystemCallError
    # ignore: socket already gone
  end
end
