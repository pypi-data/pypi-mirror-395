export class ConfigSourceResolver {
    /**
     * @param {import('./ConfigPriority.js').ConfigPriority} priority
     * @param {string | any} configSource
     */
    static addConfigs(priority: any, configSource: string | any): void;
    /**
     * @param {string} configName
     * @returns {*}
     */
    static getConfig(configName: string): any;
    static clearConfigs(): void;
    /**
     * @param {string} configSource
     * @returns {string}
     */
    static _getConfigSourceAsString(configSource: string): string;
    /**
     * @param {import('./ConfigPriority.js').ConfigPriority} priority
     * @param {string} configString
     * @returns
     */
    static _parseConfigsAndAddToCollection(priority: any, configString: string): void;
}
