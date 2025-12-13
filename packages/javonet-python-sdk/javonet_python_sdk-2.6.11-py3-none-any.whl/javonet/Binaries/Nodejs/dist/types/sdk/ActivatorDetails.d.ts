/**
 * Details for activating a type with constructor arguments
 */
export class ActivatorDetails {
    /**
     * @param {Function} type - The constructor function/class
     * @param {any[]|any} [args] - Arguments to pass to constructor (array or single value)
     */
    constructor(type: Function, args?: any[] | any);
    /** @type {Function} */
    Type: Function;
    /** @type {any[]} */
    arguments: any[];
}
