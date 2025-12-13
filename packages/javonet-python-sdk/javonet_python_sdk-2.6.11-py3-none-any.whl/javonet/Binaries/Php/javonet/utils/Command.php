<?php

declare(strict_types=1);

namespace utils;

use Exception;
use utils\type\CommandType;

final class Command implements CommandInterface
{
    private RuntimeName $runtimeName;
    private CommandType $commandType;
    /** @var array<mixed> */
    private array $payload;

    /**
     * Constructor with variadic parameters (params object[] payload in C#)
     * Also handles Array payload case - if a single array is passed, treat it as the payload
     */
    public function __construct(
        RuntimeName $runtimeName,
        CommandType $commandType,
        ...$payload
    ) {
        $this->runtimeName = $runtimeName;
        $this->commandType = $commandType;
        
        if ($payload === null || count($payload) === 0) {
            $this->payload = [];
        } elseif (count($payload) === 1 && is_array($payload[0])) {
            // Single array passed - treat it as the payload itself (Array payload case in C#)
            // Reuse array directly - no conversion overhead if it's already object[]
            $this->payload = $payload[0];
        } else {
            // Multiple arguments or non-array - treat as variadic params
            $this->payload = $payload;
        }
    }

    /**
     * @param mixed $arg
     */
    public function addArgToPayload($arg): CommandInterface
    {
        $oldLength = count($this->payload);
        $newPayload = [];
        
        if ($oldLength > 0) {
            // Copy existing payload
            foreach ($this->payload as $item) {
                $newPayload[] = $item;
            }
        }
        
        $newPayload[$oldLength] = $arg;
        
        // Pass as single array argument to match Array constructor pattern
        return new Command($this->runtimeName, $this->commandType, $newPayload);
    }

    /**
     * @param mixed $value
     */
    public function setPayload(int $index, $value): void
    {
        $this->payload[$index] = $value;
    }

    public function getRuntimeName(): RuntimeName
    {
        return $this->runtimeName;
    }

    public function getCommandType(): CommandType
    {
        return $this->commandType;
    }

    /**
     * @return array<mixed>
     */
    public function getPayload(): array
    {
        return $this->payload;
    }

    /**
     * @return mixed
     */
    public function getPayloadByIndex(int $index)
    {
        return $this->payload[$index];
    }

    public function getPayloadSize(): int
    {
        return count($this->payload);
    }

    public function toString(): string
    {
        return 'Target runtime: ' . $this->runtimeName->getName() .
            ' Command type: ' . $this->commandType->getName() .
            ' Payload: ' . json_encode($this->payload);
    }

    public function __toString(): string
    {
        try {
            $result = 'RuntimeName ';
            $result .= $this->runtimeName->getName();
            $result .= ' ';
            $result .= 'CommandType ';
            $result .= $this->commandType->getName();
            $result .= ' ';
            $result .= 'Payload ';
            
            $payload = $this->payload;
            $len = count($payload);
            
            for ($i = 0; $i < $len; $i++) {
                $item = $payload[$i];
                $result .= ($item !== null ? (string)$item : 'null');
                
                if ($i < $len - 1) {
                    $result .= ' ';
                }
            }
            
            return $result;
        } catch (Exception $e) {
            return 'Error while converting command to string:' . $e->getMessage();
        }
    }

    /**
     * @param mixed $response
     */
    public static function createResponse($response, RuntimeName $runtimeName): CommandInterface
    {
        return new Command($runtimeName, CommandType::VALUE(), $response);
    }

    public static function createReference(string $uuid, RuntimeName $runtimeName): CommandInterface
    {
        return new Command($runtimeName, CommandType::REFERENCE(), $uuid);
    }

    public static function createArrayResponse(array $array, RuntimeName $runtimeName): CommandInterface
    {
        return new Command($runtimeName, CommandType::ARRAY(), $array);
    }

    public function prependArgumentToPayload(?CommandInterface $currentCommand): CommandInterface
    {
        if ($currentCommand === null) {
            return new self($this->runtimeName, $this->commandType, $this->payload);
        }

        $oldLength = count($this->payload);
        $newPayload = [];
        
        // Put new element at the front
        $newPayload[0] = $currentCommand;
        
        if ($oldLength > 0) {
            // Copy existing payload starting from index 1
            foreach ($this->payload as $item) {
                $newPayload[] = $item;
            }
        }
        
        // Pass as single array argument to match Array constructor pattern
        return new self($this->runtimeName, $this->commandType, $newPayload);
    }

    /**
     * Drop first payload argument and return new Command
     */
    public function dropFirstPayloadArg(): CommandInterface
    {
        $payloadLength = count($this->payload);
        
        if ($payloadLength <= 1) {
            return new Command($this->runtimeName, $this->commandType);
        }
        
        $newPayload = [];
        
        // Copy from index 1 to end
        for ($i = 1; $i < $payloadLength; $i++) {
            $newPayload[] = $this->payload[$i];
        }
        
        // Pass as single array argument to match Array constructor pattern
        return new Command($this->runtimeName, $this->commandType, $newPayload);
    }

    /**
     * @param mixed $element
     */
    public function equals($element): bool
    {
        if ($this === $element) {
            return true;
        }

        if (!$element instanceof CommandInterface) {
            return false;
        }

        if ($this->runtimeName->getValue() !== $element->getRuntimeName()->getValue() || 
            $this->commandType->getValue() !== $element->getCommandType()->getValue()) {
            return false;
        }

        $elementPayload = $element->getPayload();
        if (count($this->payload) !== count($elementPayload)) {
            return false;
        }

        foreach ($this->payload as $index => $payloadItem) {
            $elementPayloadItem = $elementPayload[$index];

            if ($payloadItem instanceof CommandInterface && $elementPayloadItem instanceof CommandInterface) {
                if (!$payloadItem->equals($elementPayloadItem)) {
                    return false;
                }
                continue;
            }

            if (is_object($payloadItem) && method_exists($payloadItem, 'equals') && is_object($elementPayloadItem)) {
                if (!$payloadItem->equals($elementPayloadItem)) {
                    return false;
                }
                continue;
            }

            if ($payloadItem !== $elementPayloadItem) {
                return false;
            }
        }

        return true;
    }
}
