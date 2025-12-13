export class RegisterForUpdateHandler extends AbstractHandler {
    static _invocationContexts: {
        Value: Map<any, any>;
    };
    /**
     * Ensure context map exists and return it.
     * @returns {Map<string, any>}
     */
    static getOrCreateContextMap(): Map<string, any>;
    requiredParametersCount: number;
    /**
     * @param {any} command
     * @returns {any}
     */
    process(command: any): any;
}
import { AbstractHandler } from './AbstractHandler.js';
