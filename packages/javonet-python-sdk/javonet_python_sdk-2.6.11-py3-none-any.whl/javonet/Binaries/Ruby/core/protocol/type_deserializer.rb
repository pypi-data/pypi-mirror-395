require_relative '../../utils/string_encoding_mode_javonet'

class TypeDeserializer
  def self.deserialize_command(command_byte_array)
    Command.new(RuntimeNameJavonet(command_byte_array[0]),
                CommandType(command_byte_array[1]),
                [])
  end

  def self.deserialize_string(string_encoding_mode, encoded_string)
    raw = encoded_string.pack('C*')
    case string_encoding_mode
    when StringEncodingModeJavonet::ASCII
      raw.force_encoding('US-ASCII').encode('UTF-8')
    when StringEncodingModeJavonet::UTF8
      raw.force_encoding('UTF-8').encode('UTF-8')
    when StringEncodingModeJavonet::UTF16
      raw.force_encoding('UTF-16LE').encode('UTF-8')
    when StringEncodingModeJavonet::UTF32
      raw.force_encoding('UTF-32').encode('UTF-8')
    else
      raise 'Argument out of range in deserialize_string'
    end
  end

  def self.deserialize_int(encoded_int)
    encoded_int.pack('C*').unpack1('l<')     # 32-bit signed LE
  end

  def self.deserialize_bool(encoded_bool)
    encoded_bool[0] == 1
  end

  def self.deserialize_float(encoded_float)
    encoded_float.pack('C*').unpack1('e')    # 32-bit float LE (IEEE-754)
  end

  def self.deserialize_byte(encoded_byte)
    encoded_byte.pack('C*').unpack1('C')     # or simply encoded_byte[0]
  end

  def self.deserialize_char(encoded_char)
    encoded_char.pack('C*').unpack1('C')     # returns codepoint 0..255
  end

  def self.deserialize_longlong(encoded_long)
    encoded_long.pack('C*').unpack1('q<')    # 64-bit signed LE
  end

  def self.deserialize_double(encoded_double)
    encoded_double.pack('C*').unpack1('E')   # 64-bit double LE (IEEE-754)
  end

  def self.deserialize_ullong(encoded_ullong)
    encoded_ullong.pack('C*').unpack1('Q<')  # 64-bit unsigned LE
  end

  def self.deserialize_uint(encoded_uint)
    encoded_uint.pack('C*').unpack1('L<')    # 32-bit unsigned LE
  end

  def self.deserialize_nil(_encoded_nil)
    nil
  end
end
