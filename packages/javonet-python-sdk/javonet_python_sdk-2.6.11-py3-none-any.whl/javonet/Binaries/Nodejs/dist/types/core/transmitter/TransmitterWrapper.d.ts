export class TransmitterWrapper {
    static isNativeLibraryLoaded(): boolean;
    static loadNativeLibrary(): void;
    /**
     * @param {string} licenseKey
     */
    static activate(licenseKey: string): any;
    /**
     * @param {Uint8Array} messageArray
     * @returns {Uint8Array}
     */
    static sendCommand(messageArray: Uint8Array): Uint8Array;
    /**
     * @param {string} configSource
     */
    static setConfigSource(configSource: string): any;
    /**
     * @param {string} path
     */
    static setJavonetWorkingDirectory(path: string): void;
}
