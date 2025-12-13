require_relative 'abstract_command_handler'

class RegisterForUpdateHandler < AbstractCommandHandler
  def initialize
    @required_parameters_count = 2
  end

  def self.get_or_create_context_dict
    Thread.current[:register_for_update_handler_context] ||= {}
  end

  def process(command)
    if command.payload.length < @required_parameters_count
      raise ArgumentError.new "Register for update parameters mismatch"
    end

    obj_to_register = command.payload[0]

    guid_to_register = nil
    if command.payload.length > 1 && command.payload[1]
      guid_to_register = command.payload[1].to_s.strip.downcase
    end

    ctx = self.class.get_or_create_context_dict
    ctx[guid_to_register] = obj_to_register
    obj_to_register
  end
end
