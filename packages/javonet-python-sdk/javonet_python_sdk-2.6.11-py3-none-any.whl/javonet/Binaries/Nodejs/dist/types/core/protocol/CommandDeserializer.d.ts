export class CommandDeserializer {
    /**
     * @param {Uint8Array} byteArray
     */
    constructor(byteArray: Uint8Array);
    buffer: Uint8Array<ArrayBufferLike>;
    command: Command;
    position: number;
    /**
     * @returns {Command}
     */
    deserialize(): Command;
    isAtEnd(): boolean;
    /**
     * @param {number} typeNum
     * @returns {any}
     */
    readObject(typeNum: number): any;
    readCommand(): Command;
    readString(): string;
    readInt(): number;
    readBool(): boolean;
    readFloat(): number;
    readByte(): number;
    readChar(): number;
    readLongLong(): bigint;
    readDouble(): number;
    readUllong(): bigint;
    readUInt(): number;
    readNull(): null;
}
import { Command } from '../../utils/Command.js';
