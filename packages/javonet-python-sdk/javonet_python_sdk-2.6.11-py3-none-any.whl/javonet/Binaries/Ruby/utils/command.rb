# ruby
require_relative 'runtime_name_javonet'
require_relative 'runtime_name_handler'
require_relative 'command_type'

class Command
  attr_reader :runtime_name, :command_type, :payload

  def initialize(runtime_name, command_type, *payload)
    @runtime_name = runtime_name
    @command_type = command_type

    if payload.empty?
      @payload = []
    elsif payload.size == 1 && payload[0].is_a?(Array)
      # caller passed a single array -> reuse it (no extra copy)
      @payload = payload[0] || []
    else
      # varargs or multiple args -> use as provided
      @payload = payload
    end
  end

  def self.create_response(response, runtime_name)
    Command.new(runtime_name, CommandType::VALUE, response)
  end

  def self.create_reference(guid, runtime_name)
    Command.new(runtime_name, CommandType::REFERENCE, guid)
  end

  def self.create_array_response(array, runtime_name)
    Command.new(runtime_name, CommandType::ARRAY, array)
  end

  def drop_first_payload_argument
    return Command.new(@runtime_name, @command_type, []) if @payload.length <= 1

    new_payload = @payload[1..-1] || []
    Command.new(@runtime_name, @command_type, new_payload)
  end

  def add_arg_to_payload(argument)
    new_payload = @payload + [argument]
    Command.new(@runtime_name, @command_type, new_payload)
  end

  def prepend_arg_to_payload(arg_command)
    return self if arg_command.nil?

    new_payload = [arg_command] + @payload
    Command.new(@runtime_name, @command_type, new_payload)
  end

  def to_string
    'Runtime Library: ' + RuntimeNameHandler.get_name(@runtime_name) +
      ' ' + 'Ruby command type: ' + CommandType.get_name(@command_type).to_s +
      ' ' + 'with parameters: ' + @payload.to_s
  end

  def to_s
    to_string
  end

  def eql?(other)
    return true if equal?(other)
    return false unless other.is_a?(Command)
    return false unless runtime_name == other.runtime_name && command_type == other.command_type
    return false unless payload.length == other.payload.length

    payload.each_with_index do |item, i|
      return false unless item.eql?(other.payload[i])
    end

    true
  end

  alias == eql?
end
