<?php

declare(strict_types=1);

namespace core\webSocketClient;

use RuntimeException;
use utils\Uri as URI;

final class WebSocketClient
{
    private const SECURE_PORT_NUMBER   = 443;
    private const UNSECURE_PORT_NUMBER = 80;

    /** @var resource|null */
    private $socket = null;

    private URI $uri;
    private bool $connected = false;
    private string $secKey;

    /** ---------- Static cache & helpers (mirror Ruby) ---------- */

    /** @var array<string,WebSocketClient> */
    private static array $cache = [];

    private static function uriKey(URI $uri): string
    {
        $scheme = strtolower($uri->getScheme());
        $host   = $uri->getHost();
        $port   = $uri->getPort();
        $path   = method_exists($uri, 'isEmptyPath') && $uri->isEmptyPath() ? '/' : $uri->getPath();
        if ($path === null || $path === '') {
            $path = '/';
        }
        $query  = method_exists($uri, 'getQuery') ? $uri->getQuery() : null;

        $url = sprintf('%s://%s', $scheme, $host);
        if ($port !== null) {
            $url .= ':' . $port;
        }
        $url .= $path;
        if ($query !== null && $query !== '') {
            $url .= (strpos($url, '?') !== false ? '&' : '?') . $query;
        }
        return $url;
    }

    public static function addOrGetClient(URI $uri): WebSocketClient
    {
        $key = self::uriKey($uri);
        if (isset(self::$cache[$key]) && self::$cache[$key]->open()) {
            return self::$cache[$key];
        }
        if (isset(self::$cache[$key])) {
            self::$cache[$key]->close(true); // suppress close frame
        }
        return self::$cache[$key] = new WebSocketClient($uri);
    }

    /**
     * Sends message (array of 0..255) and returns response bytes (array<int>).
     * Reconnects once on broken/idle sockets by dropping the cached client
     * WITHOUT sending a close frame (to avoid EPIPE).
     */
    public static function sendMessage(URI $uri, array $message): array
    {
        $client = self::addOrGetClient($uri);
        try {
            $client->sendByteArray($message);
            $resp = $client->receiveByteArray();
            if ($resp === null) {
                throw new RuntimeException('No response');
            }
            return $resp;
        } catch (\Throwable $e) {
            self::closeClient($uri, true); // suppress close frame
            $client = self::addOrGetClient($uri);
            $client->sendByteArray($message);
            $resp = $client->receiveByteArray();
            if ($resp === null) {
                throw new RuntimeException('No response after reconnect');
            }
            return $resp;
        }
    }

    public static function closeClient(URI $uri, bool $suppressCloseFrame = false): void
    {
        $key = self::uriKey($uri);
        if (isset(self::$cache[$key])) {
            self::$cache[$key]->close($suppressCloseFrame);
            unset(self::$cache[$key]);
        }
    }

    /** Returns 'OPEN' | 'CLOSED' | null */
    public static function getState(URI $uri): ?string
    {
        $key = self::uriKey($uri);
        if (!isset(self::$cache[$key])) return null;
        return self::$cache[$key]->open() ? 'OPEN' : 'CLOSED';
    }

    /** ---------- Instance ---------- */

    public function __construct(URI $uri)
    {
        $this->uri    = $uri;
        $this->secKey = $this->generateWebSocketKey();

        $this->socket = $this->openSocket();
        $this->performHandshake();
        $this->connected = true;
    }

    public function __destruct()
    {
        $this->close();
    }

    public function open(): bool
    {
        if (!is_resource($this->socket)) return false;
        $meta = @stream_get_meta_data($this->socket);
        return is_array($meta) && !$meta['eof'];
    }

    /**
     * @param bool $suppressCloseFrame when true, do not attempt to send CLOSE frame
     */
    public function close(bool $suppressCloseFrame = false): void
    {
        if (is_resource($this->socket)) {
            if (!$suppressCloseFrame) {
                // Try to send CLOSE frame (0x88 0x00); ignore failures
                @fwrite($this->socket, "\x88\x00");
                @fflush($this->socket);
            }
            $this->connected = false;
            @stream_socket_shutdown($this->socket, STREAM_SHUT_RDWR);
            @fclose($this->socket);
        }
        $this->socket = null;
    }

    /** ---------- Core I/O ---------- */

    /** Send a binary message from an array of bytes (0..255) */
    private function sendByteArray(array $message): void
    {
        if (!$this->open()) {
            throw new RuntimeException('Socket not open');
        }

        // Ensure all items are 0..255 ints
        $normalized = [];
        foreach ($message as $b) {
            $normalized[] = (int)$b & 0xFF;
        }

        $payload = pack('C*', ...$normalized);
        $frame   = $this->buildClientBinaryFrame($payload);

        $this->writeAll($frame);
    }

    /**
     * Receive a single complete message as array<int>. Returns null on timeout/close.
     * Handles fragmentation and control frames (ping/pong/close).
     */
    private function receiveByteArray(int $timeoutSec = 5): ?array
    {
        $deadline = microtime(true) + $timeoutSec;
        $messagePayload = '';

        while (true) {
            $remaining = $deadline - microtime(true);
            if ($remaining <= 0) return null;

            $read = [$this->socket];
            $write = $except = [];
            $sec = (int)$remaining;
            $usec = (int)(($remaining - $sec) * 1_000_000);
            $n = @stream_select($read, $write, $except, $sec, $usec);
            if ($n === false) {
                return null;
            }
            if ($n === 0) {
                continue;
            }

            $frame = $this->readFrame();
            if ($frame === null) {
                return null; // peer closed
            }

            $opcode = $frame['opcode'];
            $fin    = $frame['fin'];
            $data   = $frame['payload'];

            switch ($opcode) {
                case 0x1: // text
                case 0x2: // binary
                case 0x0: // continuation
                    $messagePayload .= $data;
                    if ($fin) {
                        return array_values(unpack('C*', $messagePayload));
                    }
                    break;

                case 0x8: // close
                    $this->safeSendClose();
                    return null;

                case 0x9: // ping
                    $this->safeSendPong($data);
                    break;

                case 0xA: // pong
                    // ignore
                    break;

                default:
                    // ignore unknown opcode
                    break;
            }
        }
    }

    /** ---------- Handshake & framing ---------- */

    private function performHandshake(): void
    {
        $path = $this->getPathWithQuery();
        $hostHeader = $this->hostWithPort();

        $request =
            "GET {$path} HTTP/1.1\r\n" .
            "Host: {$hostHeader}\r\n" .
            "Upgrade: websocket\r\n" .
            "Connection: Upgrade\r\n" .
            "Sec-WebSocket-Key: {$this->secKey}\r\n" .
            "Sec-WebSocket-Version: 13\r\n\r\n";

        $this->writeAll($request);

        // Read HTTP response headers
        $headers = $this->readHttpHeaders(8192, 5);
        if ($headers === null) {
            throw new RuntimeException('Handshake timeout');
        }
        if (!preg_match('#^HTTP/1\.[01]\s+101#i', $headers)) {
            throw new RuntimeException('Failed to upgrade to WebSocket: ' . strtok($headers, "\r\n"));
        }

        // Validate Sec-WebSocket-Accept
        if (!preg_match('/Sec-WebSocket-Accept:\s*(.+)\r?$/mi', $headers, $m)) {
            throw new RuntimeException('Missing Sec-WebSocket-Accept');
        }
        $accept = trim($m[1]);
        $expected = base64_encode(sha1($this->secKey . '258EAFA5-E914-47DA-95CA-C5AB0DC85B11', true));
        if (!hash_equals($expected, $accept)) {
            throw new RuntimeException('Invalid Sec-WebSocket-Accept');
        }
    }

    /** Build a masked client binary frame (handles any length) */
    private function buildClientBinaryFrame(string $payload): string
    {
        $finOpcode = chr(0x80 | 0x2); // FIN + binary
        $maskBit = 0x80;

        $len = strlen($payload);
        $header = $finOpcode;

        $mask = random_bytes(4);

        if ($len < 126) {
            $header .= chr($maskBit | $len);
        } elseif ($len <= 0xFFFF) {
            $header .= chr($maskBit | 126) . pack('n', $len);
        } else {
            // 64-bit network byte order using two 32-bit words
            $hi = (int) (($len & 0xFFFFFFFF00000000) >> 32);
            $lo = (int) ($len & 0x00000000FFFFFFFF);
            $header .= chr($maskBit | 127) . pack('N2', $hi, $lo);
        }

        // Mask the payload: repeat 4-byte mask and XOR
        $repeat = (int)ceil($len / 4);
        $masked = $payload ^ str_repeat($mask, $repeat);

        return $header . $mask . substr($masked, 0, $len);
    }

    /**
     * Reads a single frame (may be control or data). Returns:
     * ['fin'=>bool,'opcode'=>int,'payload'=>string] or null on EOF.
     */
    private function readFrame(): ?array
    {
        $h = $this->readExact(2);
        if ($h === null) return null;

        $arr = unpack('C2', $h);
        $b1 = $arr[1];
        $b2 = $arr[2];

        $fin = (bool)($b1 & 0x80);
        $opcode = $b1 & 0x0F;
        $masked = (bool)($b2 & 0x80);
        $len = ($b2 & 0x7F);

        if ($len === 126) {
            $ext = $this->readExact(2);
            if ($ext === null) return null;
            $len = current(unpack('n', $ext));
        } elseif ($len === 127) {
            $ext = $this->readExact(8);
            if ($ext === null) return null;
            $parts = unpack('N2', $ext);
            $hi = $parts[1];
            $lo = $parts[2];
            $len = ($hi << 32) | $lo;
        }

        $maskKey = '';
        if ($masked) {
            // Servers should not mask; handle defensively
            $maskKey = $this->readExact(4);
            if ($maskKey === null) return null;
        }

        $payload = ($len > 0) ? ($this->readExact($len) ?? '') : '';
        if ($payload === '' && $len > 0) return null;

        if ($masked) {
            $repeat = (int)ceil($len / 4);
            $payload = $payload ^ str_repeat($maskKey, $repeat);
            $payload = substr($payload, 0, $len);
        }

        return ['fin' => $fin, 'opcode' => $opcode, 'payload' => $payload];
    }

    /** ---------- Low-level utilities ---------- */

    /** Open TCP/SSL socket; port taken from URI or defaulted by scheme like Ruby */
    private function openSocket()
    {
        $host   = $this->uri->getHost();
        $port   = $this->resolvePort();
        $scheme = $this->isSecure() ? 'ssl' : 'tcp';

        // Always create a context (PHP 7.4 requires a resource, not null)
        $opts = [];
        if ($this->isSecure()) {
            $opts = [
                'ssl' => [
                    // For production, set verify_peer => true and provide a CA bundle.
                    'verify_peer'       => false,
                    'verify_peer_name'  => false,
                    'allow_self_signed' => true,

                    // SNI
                    'peer_name'         => $host,
                    'SNI_enabled'       => true,
                ],
            ];
        }
        $ctx = stream_context_create($opts);

        $remote = sprintf('%s://%s:%d', $scheme, $host, $port);
        $errNo = 0;
        $errStr = '';

        $socket = @stream_socket_client(
            $remote,
            $errNo,
            $errStr,
            5.0,                  // connect timeout (sec)
            STREAM_CLIENT_CONNECT,
            $ctx                  // <- always a resource
        );

        if ($socket === false) {
            throw new \RuntimeException(sprintf('Could not connect to %s:%d - %s (%d)', $host, $port, $errStr, $errNo));
        }

        stream_set_blocking($socket, true);
        stream_set_timeout($socket, 5);
        return $socket;
    }

    private function readHttpHeaders(int $maxBytes, int $timeoutSec): ?string
    {
        $deadline = microtime(true) + $timeoutSec;
        $buf = '';
        while (strlen($buf) < $maxBytes) {
            $remaining = $deadline - microtime(true);
            if ($remaining <= 0) return null;

            $read = [$this->socket];
            $write = $except = [];
            $sec = (int)$remaining;
            $usec = (int)(($remaining - $sec) * 1_000_000);
            $n = @stream_select($read, $write, $except, $sec, $usec);
            if ($n === false) return null;
            if ($n === 0) continue;

            $chunk = @fread($this->socket, 1024);
            if ($chunk === '' || $chunk === false) break;
            $buf .= $chunk;

            if (strpos($buf, "\r\n\r\n") !== false) {
                return $buf;
            }
        }
        return null;
    }

    private function writeAll(string $data): void
    {
        $len = strlen($data);
        $off = 0;
        while ($off < $len) {
            $w = @fwrite($this->socket, substr($data, $off));
            if ($w === false || $w === 0) {
                throw new RuntimeException('Write failed');
            }
            $off += $w;
        }
        @fflush($this->socket);
    }

    private function readExact(int $len): ?string
    {
        $buf = '';
        while (strlen($buf) < $len) {
            $chunk = @fread($this->socket, $len - strlen($buf));
            if ($chunk === false) return null;
            if ($chunk === '') {
                $meta = @stream_get_meta_data($this->socket);
                if (!$meta || $meta['eof']) return null;
                // brief wait
                $r = [$this->socket]; $w = $e = [];
                $n = @stream_select($r, $w, $e, 1, 0);
                if ($n === 0) continue;
                if ($n === false) return null;
                continue;
            }
            $buf .= $chunk;
        }
        return $buf;
    }

    private function safeSendPong(string $payload): void
    {
        try {
            $hdr = chr(0x80 | 0xA); // FIN + pong
            $len = strlen($payload);
            if ($len < 126) {
                $hdr .= chr(0x00 | $len);
            } elseif ($len <= 0xFFFF) {
                $hdr .= chr(0x00 | 126) . pack('n', $len);
            } else {
                $hi = (int) (($len & 0xFFFFFFFF00000000) >> 32);
                $lo = (int) ($len & 0x00000000FFFFFFFF);
                $hdr .= chr(0x00 | 127) . pack('N2', $hi, $lo);
            }
            $this->writeAll($hdr . $payload);
        } catch (\Throwable $e) {
            // ignore
        }
    }

    private function safeSendClose(): void
    {
        try {
            $this->writeAll("\x88\x00");
        } catch (\Throwable $e) {
            // ignore
        }
    }

    /** ---------- URI helpers ---------- */

    private function isSecure(): bool
    {
        return strtolower($this->uri->getScheme()) === 'wss';
    }

    private function resolvePort(): int
    {
        $p = $this->uri->getPort();
        if ($p !== null) return $p;
        return $this->isSecure() ? self::SECURE_PORT_NUMBER : self::UNSECURE_PORT_NUMBER;
    }

    private function hostWithPort(): string
    {
        $host = $this->uri->getHost();
        $p = $this->uri->getPort();
        return ($p !== null) ? ($host . ':' . $p) : $host;
    }

    private function getPathWithQuery(): string
    {
        $path = method_exists($this->uri, 'isEmptyPath') && $this->uri->isEmptyPath() ? '/' : $this->uri->getPath();
        if ($path === null || $path === '') {
            $path = '/';
        }
        $query = method_exists($this->uri, 'getQuery') ? $this->uri->getQuery() : null;
        if ($query !== null && $query !== '') {
            $path .= (strpos($path, '?') !== false ? '&' : '?') . $query;
        }
        return $path;
    }

    private function generateWebSocketKey(): string
    {
        return base64_encode(random_bytes(16));
    }
}
