# frozen_string_literal: true
require_relative './runtime_name_javonet'

class RuntimeNameHandler
  def self.get_name(runtime_name)
    if runtime_name == RuntimeNameJavonet::CLR
      return 'clr'
    end
    if runtime_name == RuntimeNameJavonet::GO
      return 'go'
    end
    if runtime_name == RuntimeNameJavonet::JVM
      return 'jvm'
    end
    if runtime_name == RuntimeNameJavonet::NETCORE
      return 'netcore'
    end
    if runtime_name == RuntimeNameJavonet::PERL
      return 'perl'
    end
    if runtime_name == RuntimeNameJavonet::PYTHON
      return 'python'
    end
    if runtime_name == RuntimeNameJavonet::RUBY
      return 'ruby'
    end
    if runtime_name == RuntimeNameJavonet::NODEJS
      return 'nodejs'
    end
    if runtime_name == RuntimeNameJavonet::CPP
      return 'cpp'
    end
    if runtime_name == RuntimeNameJavonet::PHP
      return 'php'
    end
    if runtime_name == RuntimeNameJavonet::PYTHON27
      return 'python27'
    end
  end

  def self.get_runtime(name)
    if name.nil? || name.strip.empty?
      raise "Runtime name cannot be null or whitespace."
    end
    name = name.strip.downcase
    case name
    when 'clr'
      RuntimeNameJavonet::CLR
    when 'go'
      RuntimeNameJavonet::GO
    when 'jvm'
      RuntimeNameJavonet::JVM
    when 'netcore'
      RuntimeNameJavonet::NETCORE
    when 'perl'
      RuntimeNameJavonet::PERL
    when 'python'
      RuntimeNameJavonet::PYTHON
    when 'ruby'
      RuntimeNameJavonet::RUBY
    when 'nodejs'
      RuntimeNameJavonet::NODEJS
    when 'php'
      RuntimeNameJavonet::PHP
    when 'python27'
      RuntimeNameJavonet::PYTHON27
    else
      raise "#{name} is not a supported runtime."
    end
  end
end
