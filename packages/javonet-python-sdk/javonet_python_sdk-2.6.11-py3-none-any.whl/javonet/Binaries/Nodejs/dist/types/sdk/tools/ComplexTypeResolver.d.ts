export type RuntimeName = import("../../types.d.ts").RuntimeName;
export class ComplexTypeResolver {
    /**
     * Resolve type from string name and optional module
     * @param {string} typeName - Name of the type to resolve
     * @param {string} [moduleName] - Optional module name to import from
     * @returns {Function} The resolved type/constructor function
     */
    static resolveType(typeName: string, moduleName?: string): Function;
    /**
     * Attempts to extract the underlying element type from an array type string
     * @param {string} type - The type string to parse (e.g., "MyType[]")
     * @returns {string | null} Object indicating success and the element type
     * @throws {Error} If the array element type is a primitive type
     */
    static tryGetUnderlyingArrayType(type: string): string | null;
    /**
     * @param {RuntimeName} runtimeName
     * @param {string} resultType
     * @returns {any}
     */
    static tryGetTypeParsingFunction(runtimeName: RuntimeName, resultType: string): any;
    /**
     * Register a custom type mapping
     * @param {string} resultType - The type name from the target runtime
     * @param {Function} type - The JavaScript constructor function
     * @param {any[]} [args] - Default arguments for the constructor
     */
    register(resultType: string, type: Function, args?: any[]): void;
    /**
     * Convert InvocationContext result to appropriate JavaScript type
     * @param {InvocationContext} ic - The invocation context
     * @returns {Promise<any>} The converted result
     */
    convertResult(ic: InvocationContext): Promise<any>;
    /**
     * @param {string} resultType
     * @returns {ActivatorDetails | null}
     */
    tryGetValueFromTypeMap(resultType: string): ActivatorDetails | null;
    #private;
}
import { InvocationContext } from '../InvocationContext.js';
import { ActivatorDetails } from '../ActivatorDetails.js';
