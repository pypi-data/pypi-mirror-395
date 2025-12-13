export class Interpreter {
    /**
     *
     * @param {Command} command
     * @param {IConnectionData} connectionData
     * @returns {Promise<Command>}
     */
    static execute(command: Command, connectionData: IConnectionData): Promise<Command>;
    /**
     *
     * @param {Uint8Array} messageByteArray
     * @returns {Promise<Command> | Command}
     */
    static process(messageByteArray: Uint8Array): Promise<Command> | Command;
}
export type IConnectionData = import("../../utils/connectionData/IConnectionData.js").IConnectionData;
export type RuntimeNameType = typeof import("../../types.d.ts").RuntimeName;
export type Command = import("../../utils/Command.js").Command;
