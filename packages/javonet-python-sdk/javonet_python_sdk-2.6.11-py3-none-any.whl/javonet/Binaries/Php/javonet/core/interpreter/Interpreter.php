<?php

declare(strict_types=1);

namespace core\interpreter;

use core\handler\Handler;
use core\protocol\CommandDeserializer;
use core\protocol\CommandSerializer;
use core\receiver\Receiver;
use core\transmitter\Transmitter;
use core\webSocketClient\WebSocketClient;
use Exception;
use Throwable;
use utils\Command;
use utils\CommandInterface;
use utils\connectiondata\IConnectionData;
use utils\ExceptionSerializer;
use utils\messagehelper\MessageHelper;
use utils\RuntimeName;
use utils\type\ConnectionType;
use utils\Uri;

final class Interpreter
{
    private function __construct()
    {
    }

    private static function getDebugMode(): string
    {
        return getenv('DEBUG') !== false ? getenv('DEBUG') : 'FALSE';
    }

    public static function execute(CommandInterface $command, IConnectionData $IConnectionData): CommandInterface
    {
        $debugMode = self::getDebugMode();
        if ($debugMode === 'TRUE') {
            echo 'Sent command: ' . $command;
            MessageHelper::getInstance()->sendMessageToAppInsights('SentCommand', $command->toString());
        }

        $responseByteArray = self::getResponseByteArray($command, $IConnectionData);
        if ($responseByteArray instanceof Command) {
            return $responseByteArray;
        }

        $response = CommandDeserializer::deserialize($responseByteArray);
        if ($debugMode === 'TRUE') {
            echo 'Received command: ' . $response;
            MessageHelper::getInstance()->sendMessageToAppInsights('ReceivedCommand', $response->toString());
        }

        return $response;
    }

    private static function getResponseByteArray(Command $command, IConnectionData $IConnectionData)
    {
        $messageByteArray = CommandSerializer::serialize($command, $IConnectionData);
        if (self::isWebSocket($IConnectionData))
        {
            try {
                return WebSocketClient::sendMessage(new Uri($IConnectionData->getHostname()), $messageByteArray);
            } catch (Exception $e) {
                if ($e->getPrevious() instanceof Throwable) {
                    return ExceptionSerializer::serializeException($e->getPrevious(), $command);
                }

                return ExceptionSerializer::serializeException($e, $command);
            }
        }

        if (self::isInMemoryAndSameRuntime($command, $IConnectionData)) {
            return Receiver::sendCommand($messageByteArray);
        }

        return Transmitter::sendCommand($messageByteArray);
    }

    private static function isWebSocket(IConnectionData $IConnectionData): bool
    {
        return $IConnectionData->getConnectionType()->equalsByValue(ConnectionType::WEB_SOCKET);
    }

    private static function isInMemoryAndSameRuntime(Command $command, IConnectionData $IConnectionData): bool
    {
        return $command->getRuntimeName()->equalsByValue(RuntimeName::PHP)
            && $IConnectionData->getConnectionType()->equalsByValue(ConnectionType::IN_MEMORY);
    }

    public static function process(array $byteArray): CommandInterface
    {
        $debugMode = self::getDebugMode();
        $receivedCommand = CommandDeserializer::deserialize($byteArray);
        if ($debugMode === 'TRUE') {
            echo 'Received command: ' . $receivedCommand;
            MessageHelper::getInstance()->sendMessageToAppInsights('ReceivedCommand', $receivedCommand->toString());
        }

        $response = Handler::handleCommand($receivedCommand);
        if ($debugMode === 'TRUE') {
            echo 'Response command: ' . $response;
            MessageHelper::getInstance()->sendMessageToAppInsights('ResponseCommand', $response->toString());
        }

        return $response;
    }
}
