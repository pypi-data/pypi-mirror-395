export type RuntimeName = import("../../types.d.ts").RuntimeName;
export class Handler {
    static _initialized: boolean;
    /**
     * Initializes the handlers map. This is called lazily on first use.
     */
    static _initialize(): void;
    /**
     * @param {Command} command
     * @returns {Promise<Command> | Command}
     */
    static handleCommand(command: Command): Promise<Command> | Command;
    /**
     * Prefer innerException (or cause) when available.
     * @param {any} error
     * @param {Command} command
     * @returns {Command}
     */
    static resolveException(error: any, command: Command): Command;
    /**
     * @param {any} response
     * @param {RuntimeName} runtimeName
     * @returns {Promise<Command> | Command}
     */
    static parseCommand(response: any, runtimeName: RuntimeName): Promise<Command> | Command;
}
/**
 * @typedef {import('../../types.d.ts').RuntimeName} RuntimeName
 */
/**
 * @type {Record<number, AbstractHandler>}
 */
export const handlers: Record<number, AbstractHandler>;
import { Command } from '../../utils/Command.js';
import { AbstractHandler } from './AbstractHandler.js';
