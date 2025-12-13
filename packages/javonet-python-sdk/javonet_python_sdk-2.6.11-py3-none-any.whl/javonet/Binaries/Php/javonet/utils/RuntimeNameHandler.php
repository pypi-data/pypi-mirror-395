<?php

declare(strict_types=1);

namespace utils;

final class RuntimeNameHandler
{
    public static function getName(RuntimeName $runtimeName): string
    {
        switch ($runtimeName->getValue()) {
            case RuntimeName::CLR:
                return 'clr';
            case RuntimeName::GO:
                return 'go';
            case RuntimeName::JVM:
                return 'jvm';
            case RuntimeName::NETCORE:
                return 'netcore';
            case RuntimeName::PERL:
                return 'perl';
            case RuntimeName::PYTHON:
                return 'python';
            case RuntimeName::RUBY:
                return 'ruby';
            case RuntimeName::NODEJS:
                return 'nodejs';
            case RuntimeName::CPP:
                return 'cpp';
            case RuntimeName::PHP:
                return 'php';
            case RuntimeName::PYTHON27:
                return 'python27';
            case RuntimeName::NONE:
                return 'none';
            default:
                 throw new \Exception('Invalid runtime name.');
        }
    }

    public static function getRuntimeName(string $runtime): RuntimeName
    {
        switch (strtolower($runtime)) {
            case 'clr':
                return new RuntimeName(RuntimeName::CLR);
            case 'go':
                return new RuntimeName(RuntimeName::GO);
            case 'jvm':
                return new RuntimeName(RuntimeName::JVM);
            case 'netcore':
                return new RuntimeName(RuntimeName::NETCORE);
            case 'perl':
                return new RuntimeName(RuntimeName::PERL);
            case 'python':
                return new RuntimeName(RuntimeName::PYTHON);
            case 'ruby':
                return new RuntimeName(RuntimeName::RUBY);
            case 'nodejs':
                return new RuntimeName(RuntimeName::NODEJS);
            case 'cpp':
                return new RuntimeName(RuntimeName::CPP);
            case 'php':
                return new RuntimeName(RuntimeName::PHP);
            case 'python27':
                return new RuntimeName(RuntimeName::PYTHON27);
            case 'none':
                return new RuntimeName(RuntimeName::NONE);
            default:
                 throw new \Exception('Invalid runtime name string.');
        }
    }
}
