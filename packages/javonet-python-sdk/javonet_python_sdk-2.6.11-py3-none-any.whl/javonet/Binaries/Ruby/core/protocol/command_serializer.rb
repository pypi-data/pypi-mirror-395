require_relative 'type_serializer'
require_relative '../../utils/command'
require_relative '../../utils/runtime_name_javonet'
require_relative '../../utils/tcp_connection_data'

class CommandSerializer
  def self.serialize(root_command, connection_data = nil, runtime_version = 0)
    buffer = ''.dup
    buffer << [root_command.runtime_name, runtime_version].pack('C*')

    if connection_data
      buffer << connection_data.serialize_connection_data.pack('C*')
    else
      buffer << [0, 0, 0, 0, 0, 0, 0].pack('C*')
    end
    buffer << [RuntimeNameJavonet::RUBY, root_command.command_type].pack('C*')

    # Payload (recursive)
    serialize_recursively(root_command, buffer)

    buffer.bytes
  end

  private

  def self.serialize_recursively(command, buffer)
    command.payload.each do |item|
      if item.is_a?(Command)
        buffer << TypeSerializer.serialize_command(item).pack('C*')
        serialize_recursively(item, buffer)
      else
        buffer << TypeSerializer.serialize_primitive(item).pack('C*')
      end
    end
  end
end
