require_relative '../../utils/type'
require_relative '../../utils/string_encoding_mode_javonet'

class TypeSerializer
  def self.serialize_primitive(payload_item)
    if payload_item.nil?
      serialize_nil
    elsif [true, false].include?(payload_item)
      serialize_bool(payload_item)
    elsif payload_item.is_a?(Integer)
      if (-2**31..2**31 - 1).include?(payload_item)
        serialize_int(payload_item)
      elsif (-2**63..2**63 - 1).include?(payload_item)
        serialize_longlong(payload_item)
      else
        serialize_ullong(payload_item)
      end
    elsif payload_item.is_a?(String)
      serialize_string(payload_item)
    elsif payload_item.is_a?(Float)
      serialize_double(payload_item)
    elsif payload_item.is_a?(FalseClass) || payload_item.is_a?(TrueClass)
      serialize_bool(payload_item)
    else
      raise TypeError, "Unsupported payload item type: #{payload_item.class} for payload item: #{payload_item}."
    end
  end

  def self.serialize_command(command)
    length = int_to_bytes(command.payload.length)
    [Type::COMMAND] + length + [command.runtime_name, command.command_type]
  end

  def self.serialize_string(string_value)
    encoded_string_list = string_value.bytes
    length = int_to_bytes(encoded_string_list.length)
    [Type::JAVONET_STRING, StringEncodingModeJavonet::UTF8] + length + encoded_string_list
  end

  def self.serialize_int(int_value)
    encoded_int_list = int_to_bytes(int_value)
    [Type::JAVONET_INTEGER, encoded_int_list.length] + encoded_int_list
  end

  def self.serialize_bool(bool_value)
    encoded_bool_list = bool_value ? [1] : [0]
    [Type::JAVONET_BOOLEAN, encoded_bool_list.length] + encoded_bool_list
  end

  def self.serialize_float(float_value)
    encoded_float_list = float_to_bytes(float_value)
    [Type::JAVONET_FLOAT, encoded_float_list.length] + encoded_float_list
  end

  def self.serialize_byte(byte_value)
    encoded_byte_list = [byte_value].pack('C').bytes
    [Type::JAVONET_BYTE, encoded_byte_list.length] + encoded_byte_list
  end

  def self.serialize_char(char_value)
    encoded_char_list = [char_value].pack('C').bytes
    [Type::JAVONET_CHAR, encoded_char_list.length] + encoded_char_list
  end

  def self.serialize_longlong(longlong_value)
    encoded_longlong_list = longlong_to_bytes(longlong_value)
    [Type::JAVONET_LONG_LONG, encoded_longlong_list.length] + encoded_longlong_list
  end

  def self.serialize_double(double_value)
    encoded_double_list = double_to_bytes(double_value)
    [Type::JAVONET_DOUBLE, encoded_double_list.length] + encoded_double_list
  end

  def self.serialize_uint(uint_value)
    encoded_uint_list = uint_to_bytes(uint_value)
    [Type::JAVONET_UNSIGNED_INTEGER, encoded_uint_list.length] + encoded_uint_list
  end

  def self.serialize_ullong(ullong_value)
    encoded_ullong_list = ullong_to_bytes(ullong_value)
    [Type::JAVONET_UNSIGNED_LONG_LONG, encoded_ullong_list.length] + encoded_ullong_list
  end

  def self.serialize_nil
    [Type::JAVONET_NULL, 1, 0]
  end

  # -------- pack(...).bytes helpers (little-endian) --------

  # 32-bit signed int → LE bytes
  def self.int_to_bytes(value)
    [value].pack('l<').bytes
  end

  # 32-bit unsigned int → LE bytes
  def self.uint_to_bytes(value)
    [value].pack('L<').bytes
  end

  # 64-bit signed → LE bytes
  def self.longlong_to_bytes(value)
    [value].pack('q<').bytes
  end

  # 64-bit unsigned → LE bytes
  def self.ullong_to_bytes(value)
    [value].pack('Q<').bytes
  end

  # 32-bit IEEE-754 float → LE bytes
  def self.float_to_bytes(value)
    [value].pack('e').bytes   # little-endian float
  end

  # 64-bit IEEE-754 double → LE bytes
  def self.double_to_bytes(value)
    [value].pack('E').bytes   # little-endian double
  end
end
