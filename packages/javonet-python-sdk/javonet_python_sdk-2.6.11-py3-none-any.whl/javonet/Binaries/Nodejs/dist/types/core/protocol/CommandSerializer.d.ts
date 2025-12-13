export type IConnectionData = import("../../utils/connectionData/IConnectionData.js").IConnectionData;
/**
 * @typedef {import('../../utils/connectionData/IConnectionData.js').IConnectionData} IConnectionData
 */
export class CommandSerializer {
    /**
     * Serializes the root command with connection data and optional runtime version.
     * @param {Command} rootCommand
     * @param {IConnectionData} connectionData
     * @param {number} runtimeVersion
     * @returns {Uint8Array}
     */
    static serialize(rootCommand: Command, connectionData: IConnectionData, runtimeVersion?: number): Uint8Array;
    /**
     * Recursively serializes command payload.
     * @param {Command} command
     * @param {Array<Uint8Array>} buffers
     */
    static serializeRecursively(command: Command, buffers: Array<Uint8Array>): void;
}
import { Command } from '../../utils/Command.js';
