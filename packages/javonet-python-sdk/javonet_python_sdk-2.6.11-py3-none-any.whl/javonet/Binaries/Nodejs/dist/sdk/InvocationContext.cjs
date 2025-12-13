"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);
var InvocationContext_exports = {};
__export(InvocationContext_exports, {
  InvocationContext: () => InvocationContext
});
module.exports = __toCommonJS(InvocationContext_exports);
var import_DelegatesCache = require("../core/delegatesCache/DelegatesCache.cjs");
var import_Interpreter = require("../core/interpreter/Interpreter.cjs");
var import_Command = require("../utils/Command.cjs");
var import_CommandType = require("../utils/CommandType.cjs");
var import_ExceptionThrower = require("../utils/exception/ExceptionThrower.cjs");
var import_RuntimeName = require("../utils/RuntimeName.cjs");
var import_TypesHandler = require("../utils/TypesHandler.cjs");
var import_uuid = require("uuid");
class AsyncLock {
  constructor() {
    this._tail = Promise.resolve();
  }
  async lock() {
    let release;
    const prev = this._tail;
    this._tail = new Promise((res) => release = res);
    await prev;
    return () => release(void 0);
  }
}
class InvocationContext {
  /** @type {RuntimeNameType} */
  #runtimeName;
  /** @type {IConnectionData} */
  #connectionData;
  /** @type {Command | null} */
  #currentCommand = null;
  /** @type {Command | null} */
  #responseCommand = null;
  /** @type {boolean} */
  #isExecuted = false;
  /** @type {string | null} */
  #guid = null;
  /** @type {AsyncLock} */
  #materializationLock = new AsyncLock();
  // Static map holding contexts waiting for materialization (guid -> InvocationContext)
  static _invocationContexts = /* @__PURE__ */ new Map();
  //
  /**
   *
   * @param {RuntimeNameType} runtimeName
   * @param {IConnectionData} connectionData
   * @param {Command} command
   * @param {boolean} isExecuted
   */
  constructor(runtimeName, connectionData, command, isExecuted = false) {
    this.#runtimeName = runtimeName;
    this.#connectionData = connectionData;
    this.#currentCommand = command;
    this.#responseCommand = null;
    this.#isExecuted = isExecuted;
    this.#guid = (0, import_uuid.v4)();
  }
  /**
   * @returns {string} guid of this InvocationContext
   */
  getGuid() {
    return this.#guid;
  }
  /**
   * @param {Command} localCommand
   * @returns {InvocationContext}
   */
  #createInstanceContext(localCommand) {
    return new InvocationContext(
      this.#runtimeName,
      this.#connectionData,
      this.#buildCommand(localCommand)
    );
  }
  /**
   * @returns {Command|null}
   */
  getCurrentCommand() {
    return this.#currentCommand;
  }
  //destructor() {
  //    if (this.#currentCommand.commandType === CommandType.Reference) {
  //        this.#currentCommand = new Command(
  //            this.#runtimeName,
  //            CommandType.DestructReference,
  //            this.#currentCommand.payload
  //        );
  //        this.execute();
  //    }
  //}
  /**
   * Async iterator for InvocationContext arrays
   * Use: for await (const item of invocationContext) { ... }
   * @returns {AsyncGenerator<InvocationContext, void, unknown>}
   */
  async *[Symbol.asyncIterator]() {
    if (this.#currentCommand?.commandType !== import_CommandType.CommandType.Reference) {
      throw new Error("Object is not iterable");
    }
    const sizeCtx = await this.getSize().execute();
    const arraySize = Number(sizeCtx.getValue());
    for (let position = 0; position < arraySize; position++) {
      yield this.getIndex(position);
    }
  }
  /**
   * Executes the current command.
   * Returns the InvocationContext after executing the command.
   * @returns {Promise<InvocationContext>}
   * @method
   */
  async execute() {
    if (this.#currentCommand === null) {
      throw new Error("currentCommand is undefined in Invocation Context execute method");
    }
    const entries = Array.from(InvocationContext._invocationContexts.entries());
    entries.sort((a, b) => String(a[0]).localeCompare(String(b[0])));
    const releases = [];
    for (const [, ic] of entries) {
      const release = await ic.#materializationLock.lock();
      releases.push(release);
    }
    try {
      this.#responseCommand = await import_Interpreter.Interpreter.execute(
        this.#currentCommand,
        this.#connectionData
      );
      if (!this.#responseCommand) {
        throw new Error("responseCommand is undefined in Invocation Context execute method");
      }
      if (this.#responseCommand.commandType === import_CommandType.CommandType.Exception) {
        throw import_ExceptionThrower.ExceptionThrower.throwException(this.#responseCommand);
      }
      this.#responseCommand = this.#processUpdateInvocationContextCommands(this.#responseCommand);
      if (this.#responseCommand.commandType === import_CommandType.CommandType.CreateClassInstance) {
        this.#currentCommand = this.#responseCommand;
        this.#isExecuted = true;
        return this;
      }
      return new InvocationContext(this.#runtimeName, this.#connectionData, this.#responseCommand, true);
    } finally {
      for (let i = releases.length - 1; i >= 0; i--) {
        try {
          releases[i]();
        } catch {
        }
      }
    }
  }
  /**
   * Process UpdateInvocationContext commands in the provided responseCommand payload.
   * For each ValueForUpdate command, set the referenced InvocationContext's currentCommand to a Reference command,
   * remove that InvocationContext from the static map and remove ValueForUpdate items from response payload.
   * @param {Command} responseCommand
   * @returns {Command}
   */
  #processUpdateInvocationContextCommands(responseCommand) {
    if (!responseCommand?.payload || responseCommand.payload.length === 0) {
      return responseCommand;
    }
    const commandsToUpdate = [];
    for (const item of responseCommand.payload) {
      if (item instanceof import_Command.Command && item.commandType === import_CommandType.CommandType.ValueForUpdate) {
        commandsToUpdate.push(item);
      }
    }
    if (commandsToUpdate.length === 0) {
      return responseCommand;
    }
    const updatedPayload = Array.from(responseCommand.payload);
    for (const cmd of commandsToUpdate) {
      const cmdPayload = cmd.payload;
      if (cmdPayload && cmdPayload.length >= 2) {
        const contextGuid = String(cmdPayload[0]);
        const instanceGuid = String(cmdPayload[1]);
        const invCtx = InvocationContext._invocationContexts.get(contextGuid);
        if (invCtx) {
          invCtx.#currentCommand = new import_Command.Command(invCtx.#runtimeName, import_CommandType.CommandType.Reference, [instanceGuid]);
          InvocationContext._invocationContexts.delete(contextGuid);
        }
      }
      const idx = updatedPayload.indexOf(cmd);
      if (idx >= 0) updatedPayload.splice(idx, 1);
    }
    return new import_Command.Command(responseCommand.runtimeName, responseCommand.commandType, updatedPayload);
  }
  /**
   * Invokes a static method on the target runtime.
   * @param {string} methodName - The name of the method to invoke.
   * @param {...any} args - Method arguments.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to invoke the static method.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/calling-methods/invoking-static-method)
   * @method
   */
  invokeStaticMethod(methodName, ...args) {
    let localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.InvokeStaticMethod, [
      methodName,
      ...args
    ]);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Retrieves the value of a static field from the target runtime.
   * @param {string} fieldName - The name of the field to get.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to get the static field.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/fields-and-properties/getting-and-setting-values-for-static-fields-and-properties)
   * @method
   */
  getStaticField(fieldName) {
    let localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.GetStaticField, [fieldName]);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Sets the value of a static field in the target runtime.
   * @param {string} fieldName - The name of the field to set.
   * @param {any} value - The new value of the field.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to set the static field.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/fields-and-properties/getting-and-setting-values-for-static-fields-and-properties)
   * @method
   */
  setStaticField(fieldName, value) {
    let localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.SetStaticField, [fieldName, value]);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Creates a new instance of a class in the target runtime.
   * Adds the newly created context to the static invocation contexts map and
   * includes the context GUID as the first argument of CreateClassInstance command payload.
   * @param {...any} args - The arguments to pass to the class constructor
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to create the instance.
   * @method
   */
  createInstance(...args) {
    const localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.CreateClassInstance, [...args]);
    const createInstanceInvCtx = this.#createInstanceContext(localCommand);
    return createInstanceInvCtx.#registerForUpdate();
  }
  /**
   * Registers the current InvocationContext for updates.
   * @returns {InvocationContext}
   */
  #registerForUpdate() {
    this.#currentCommand = this.#buildCommand(new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.RegisterForUpdate, [this.getGuid()]));
    InvocationContext._invocationContexts.set(this.getGuid(), this);
    return this;
  }
  /**
   * Retrieves the value of an instance field from the target runtime.
   * @param {string} fieldName - The name of the field to get.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to get the instance field.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/fields-and-properties/getting-and-setting-values-for-instance-fields-and-properties)
   * @method
   */
  getInstanceField(fieldName) {
    let localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.GetInstanceField, [fieldName]);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Sets the value of an instance field in the target runtime.
   * @param {string} fieldName - The name of the field to set.
   * @param {any} value - The new value of the field.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to set the instance field.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/fields-and-properties/getting-and-setting-values-for-instance-fields-and-properties)
   * @method
   */
  setInstanceField(fieldName, value) {
    let localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.SetInstanceField, [fieldName, value]);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Invokes an instance method on the target runtime.
   * @param {string} methodName - The name of the method to invoke.
   * @param {...any} args - Method arguments.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to invoke the instance method.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/calling-methods/invoking-instance-method)
   * @method
   */
  invokeInstanceMethod(methodName, ...args) {
    let localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.InvokeInstanceMethod, [
      methodName,
      ...args
    ]);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Retrieves the value at a specific index in an array from the target runtime.
   * @param {...any} indexes - the arguments to pass to the array getter. The first argument should be the index.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to get the index.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/arrays-and-collections/one-dimensional-arrays)
   * @method
   */
  getIndex(...indexes) {
    let localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.ArrayGetItem, indexes);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Sets the value at a specific index in an array in the target runtime.
   * @param {number[]} indexes - The index to set the value at.
   * @param {any} value - The value to set at the index.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to set the index.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/arrays-and-collections/one-dimensional-arrays)
   * @method
   */
  setIndex(indexes, value) {
    let localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.ArraySetItem, [indexes, value]);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Retrieves the size of an array from the target runtime.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to get the size.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/arrays-and-collections/one-dimensional-arrays)
   * @method
   */
  getSize() {
    let localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.ArrayGetSize, []);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Retrieves the rank of an array from the target runtime.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to get the rank.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/arrays-and-collections/one-dimensional-arrays)
   * @method
   */
  getRank() {
    let localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.ArrayGetRank, []);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Invokes a generic static method on the target runtime.
   * @param {string} methodName - The name of the method to invoke.
   * @param {...any} args - Method arguments.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to invoke the generic static method.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/generics/calling-generic-static-method)
   * @method
   */
  invokeGenericStaticMethod(methodName, ...args) {
    let localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.InvokeGenericStaticMethod, [
      methodName,
      ...args
    ]);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Invokes a generic method on the target runtime.
   * @param {string} methodName - The name of the method to invoke.
   * @param {...any} args - Method arguments.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to invoke the generic method.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/generics/calling-generic-instance-method)
   * @method
   */
  invokeGenericMethod(methodName, ...args) {
    let localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.InvokeGenericMethod, [
      methodName,
      ...args
    ]);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Retrieves the name of an enum from the target runtime.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to get the enum name.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/enums/using-enum-type)
   * @method
   */
  getEnumName() {
    let localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.GetEnumName, []);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Retrieves the value of an enum from the target runtime.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to get the enum value.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/enums/using-enum-type)
   * @method
   */
  getEnumValue() {
    let localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.GetEnumValue, []);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Retrieves the value of a reference from the target runtime.
   * @returns {InvocationContext} A new InvocationContext instance that wraps the command to get the ref value.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/methods-arguments/passing-arguments-by-reference-with-ref-keyword)
   * @method
   */
  getRefValue() {
    let localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.GetRefValue, []);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Creates a null object of a specific type on the target runtime.
   *
   * @returns {InvocationContext} An InvocationContext instance with the command to create a null object.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/null-handling/create-null-object)
   * @method
   */
  createNull() {
    let localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.CreateNull, []);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Creates a null object of a specific type on the target runtime.
   * @param {string} methodName - The name of the method to invoke.
   * @param {...any} args - Method arguments.
   * @returns {InvocationContext} An InvocationContext instance with the command to create a null object.
   * TODO: connect documentation page url
   * @see [Javonet Guides](https://www.javonet.com/guides/)
   * @method
   */
  getStaticMethodAsDelegate(methodName, ...args) {
    const localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.GetStaticMethodAsDelegate, [
      methodName,
      ...args
    ]);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Creates a null object of a specific type on the target runtime.
   * @param {string} methodName - The name of the method to invoke.
   * @param {...any} args - Method arguments.
   * @returns {InvocationContext} An InvocationContext instance with the command to create a null object.
   * TODO: connect documentation page url
   * @see [Javonet Guides](https://www.javonet.com/guides/)
   * @method
   */
  getInstanceMethodAsDelegate(methodName, ...args) {
    const localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.GetInstanceMethodAsDelegate, [
      methodName,
      ...args
    ]);
    return this.#createInstanceContext(localCommand);
  }
  /**
   * Retrieves the type of the object from the target runtime.
   * @returns {Promise<string>} The type of the object.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/type-handling/getting-object-type)
   * @method
   */
  async getResultType() {
    const localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.GetResultType, []);
    const invocationContext = new InvocationContext(
      this.#runtimeName,
      this.#connectionData,
      this.#buildCommand(localCommand)
    );
    const execCtx = await invocationContext.execute();
    return String(execCtx.getValue());
  }
  /**
   * Retrieves the name of the runtime where the command is executed.
   * @returns {number} The name of the runtime.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/runtime-name)
   * @method
   */
  getRuntimeName() {
    return this.#runtimeName;
  }
  /**
   * Retrieves an array from the target runtime.
   * @async
   * @returns {Promise<any[]>}
   * @method
   */
  async retrieveArray() {
    const localCommand = new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.RetrieveArray, []);
    const localInvCtx = new InvocationContext(
      this.#runtimeName,
      this.#connectionData,
      this.#buildCommand(localCommand)
    );
    await localInvCtx.execute();
    const resolve = (item) => {
      return item?.commandType === import_CommandType.CommandType.Reference ? new InvocationContext(
        this.#runtimeName,
        this.#connectionData,
        item
      ) : item;
    };
    const respCommand = localInvCtx.#responseCommand;
    if (!respCommand) {
      return [];
    }
    if (respCommand.payload) {
      return respCommand.payload.map((item) => resolve(item));
    }
    return respCommand.payload || [];
  }
  /**
   * Returns the primitive value from the target runtime. This could be any primitive type in JavaScript,
   * such as int, boolean, byte, char, long, double, float, etc.
   * @returns {unknown} The value of the current command.
   * @see [Javonet Guides](https://www.javonet.com/guides/v2/javascript/foundations/execute-method)
   * @method
   */
  getValue() {
    return this.#currentCommand?.payload[0];
  }
  /**
   * @param {Command} command
   * @returns {Command}
   */
  #buildCommand(command) {
    for (let i = 0; i < command.payload.length; i++) {
      command.payload[i] = this.#encapsulatePayloadItem(command.payload[i]);
    }
    return command.prependArgToPayload(this.#currentCommand);
  }
  /**
   * @param {unknown} payloadItem
   * @returns {Command|null}
   */
  #encapsulatePayloadItem(payloadItem) {
    if (payloadItem instanceof import_Command.Command) {
      for (let i = 0; i < payloadItem.payload.length; i++) {
        payloadItem.payload[i] = this.#encapsulatePayloadItem(payloadItem.payload[i]);
      }
      return payloadItem;
    } else if (payloadItem instanceof InvocationContext) {
      return payloadItem.getCurrentCommand();
    } else if (payloadItem instanceof Array) {
      const copiedArray = payloadItem.map((item) => this.#encapsulatePayloadItem(item));
      return new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.Array, copiedArray);
    } else if (typeof payloadItem === "function") {
      let newArray = new Array(payloadItem.length + 1);
      for (let i = 0; i < newArray.length; i++) {
        newArray[i] = typeof Object;
      }
      const args = [import_DelegatesCache.delegatesCacheInstance.addDelegate(payloadItem), import_RuntimeName.RuntimeName.Nodejs];
      args.push(...newArray);
      return new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.PassDelegate, args);
    } else if (import_TypesHandler.TypesHandler.isPrimitiveOrNullOrUndefined(payloadItem)) {
      return new import_Command.Command(this.#runtimeName, import_CommandType.CommandType.Value, [payloadItem]);
    } else {
      throw Error(
        "Unsupported payload item type: " + (payloadItem?.constructor?.name || typeof payloadItem) + " for payload item: " + payloadItem
      );
    }
  }
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  InvocationContext
});
