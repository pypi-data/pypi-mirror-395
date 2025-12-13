export class Transmitter {
    /**
     * @param {Uint8Array} messageArray
     * @returns {Uint8Array}
     */
    static sendCommand(messageArray: Uint8Array): Uint8Array;
    /**
     * @param {string} licenseKey
     * @returns {void}
     */
    static activate(licenseKey: string): void;
    /**
     * @param {string} configSource
     * @returns {void}
     */
    static setConfigSource(configSource: string): void;
    /**
     * @param {string} workingDirectory
     * @returns
     */
    static setJavonetWorkingDirectory(workingDirectory: string): void;
}
