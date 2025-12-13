/**
 * Details for activating a type with constructor arguments
 */
export class Activator {
    /**
     * Create a new instance of a type
     * @param {Function} Type - The constructor function/class
     * @param {any[] | any} args - The arguments to pass to the constructor
     * @returns {any} The new instance
     */
    static createInstance(Type: Function, args: any[] | any): any;
}
