<?php

declare(strict_types=1);

namespace core\receiver;

use core\interpreter\Interpreter;
use core\protocol\CommandSerializer;


use Throwable;
use utils\Command;
use utils\ExceptionSerializer;
use utils\RuntimeLogger;
use utils\RuntimeName;
use utils\type\CommandType;

final class Receiver
{
    private function __construct()
    {
    }

    public static function sendCommand(array $messageByteArray): array
    {
        try {
            $result = Interpreter::process($messageByteArray);
            return CommandSerializer::serialize($result, null);
        } catch (Throwable $ex) {
            $exceptionCommand = ExceptionSerializer::serializeException(
                $ex,
                new Command(RuntimeName::PHP(), CommandType::EXCEPTION(), [])
            );
            return CommandSerializer::serialize($exceptionCommand, null);
        }
    }

    public static function heartBeat(array $messageByteArray): array
    {
        return [$messageByteArray[11], $messageByteArray[12] - 2];
    }

    public static function getRuntimeInfo(): string
    {
        return RuntimeLogger::getRuntimeInfo();
    }
}
