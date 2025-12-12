// Base.ts
/** @module Base */

// @ts-ignore
import * as React from 'react';
import * as t from './types';


type ModuleResolve = (names: string[]) => Promise<t.StringKeyedObject>;
type CopyImportPool = () => ImportPool;

/**
 * @typedef ImportPool
 *
 * Is a :js:data:`StringKeyedObject` containing Promise(es)
 * to resolve to a module.
 */
export interface ImportPool {
    [propertyName: string]: Promise<t.StringKeyedObject> | ModuleResolve | CopyImportPool;
    copy?: CopyImportPool;
    resolve?: ModuleResolve;
}

export interface IImportPoolRegistry {
    modulePromises: ImportPool;
    resolve: ModuleResolve;
    copy: CopyImportPool;
}


/**
 * Each lino module must have an instance of this class
 * pointed to by the module level constant :js:data:`exModulePromises`
 */
export class ImportPoolRegistry implements IImportPoolRegistry {
    modulePromises: ImportPool;
    resolve: ModuleResolve = async (names) => {
        const values = {};
        for (const name of names) {
            if (!(name in this.modulePromises)) {
                throw new Error(`ImportPoolRegistry: Module '${name}' not found in the import pool.`);
            }
            values[name] = await (this.modulePromises[name] as Promise<t.StringKeyedObject>).then(mod => mod);
        }
        return values;
    }

    copy: CopyImportPool = () => {
        const copy = {...this.modulePromises};
        delete copy.copy;
        delete copy.resolve;
        return copy;
    }

    constructor(module_exModulePromises: ImportPool) {
        this.resolve = this.resolve.bind(this);
        this.copy = this.copy.bind(this);
        this.modulePromises = module_exModulePromises;
        module_exModulePromises.resolve = this.resolve;
        module_exModulePromises.copy = this.copy;
    }
}
export function RegisterImportPool(mem: ImportPool) {return new ImportPoolRegistry(mem)}


const exModulePromises = {};
RegisterImportPool(exModulePromises);


/** A hook for function components to resolve the required modules. */
export function getExReady(
    module_exModulePromises: ImportPool, names: string[],
    finalize = (mods: t.StringKeyedObject): t.StringKeyedObject => null
): t.StringKeyedObject {
    const [localEx, setLocalEx] = React.useState<t.ObjectAny>({ready: false});
    React.useEffect(() => {
        if (!localEx.ready) (module_exModulePromises.resolve as ModuleResolve)(names).then(mods => {
            finalize(mods);
            setLocalEx(Object.assign(mods, {ready: true}));
        })}, []);
    return localEx;
}

/**
 * Dynamic Dependencies (DynDep)
 *
 * The code block that suppose to go to the `constructor` of subclasses
 * should be put into the overridden :js:meth:`onReady` method.
 *
 */
export class DynDep implements t.DynDepBase {
    static requiredModules: string[] = [];
    static iPool: ImportPool = exModulePromises;
    exModules: t.StringKeyedObject;
    ex: t.StringKeyedObject;
    ready: boolean = false;
    /** Executes after the module import resolves and :js:meth:`DynDep.prepare` finishes. */
    onReady(params) {}
    /** Executes after the module import resolves. */
    async prepare(): Promise<void> {}
    /**
     * Resolves :js:attr:`DynDep.requiredModules` and put them
     * into :js:attr:`DynDep.exModules`.
     */
    private resolveImports = async (): Promise<void> => {
        Object.assign(this.ex, await ((<typeof DynDep>this.constructor).iPool.resolve as ModuleResolve)(
            ((<typeof DynDep>this.constructor).requiredModules)));
        await this.prepare();
    }

    /** Sets the state `ready` to `true` and calls :meth:`onReady`. */
    private setReady = (params): void => {
        this.ready = true;
        this.onReady(params);
    }
    /**
     * WARNING: Advised to not override this method in subclasses instead
     * override :meth:`onReady`.
     */
    constructor(params) {
        /** Dynamically imported modules are put into this attribute. */
        this.exModules = {};
        /** A shorthand reference to the :attr:`exModules`. */
        this.ex = this.exModules;

        this.resolveImports = this.resolveImports.bind(this);
        this.setReady = this.setReady.bind(this);

        this.resolveImports().then(() => this.setReady(params));
    }
}


/**
 * Extends React.Component
 *
 * Helps in rendering lazyly, as in - components that renders
 * some dynamically imported component could wait for the
 * the state `ready` to become `true`.
 *
 * All the life-cycle methods of a subclass of this type
 * must check for state `ready` before trying in modifying
 * any other state.
 */
export class Component extends React.Component implements t.DynDep {
    static requiredModules: string[] = [];
    static iPool: ImportPool = exModulePromises;
    exModules: t.StringKeyedObject;
    ex: t.StringKeyedObject;
    state: t.ObjectAny;
    setState: any;
    /**
     * WARNING: Advised to not override this method in subclasses instead
     * override :meth:`onReady`.
     */
    componentDidMount() {
        this.resolveImports().then(() => this.setReady());
    }

    /**
     * Executes after the component state becomes `ready`.
     * Substitues React.Component.componentDidMount feature
     * as advised to use onReady instead.
     */
    onReady() {}

    /** @see :js:meth:`DynDep.prepare` */
    async prepare(): Promise<void> {}

    /**
     * @see :js:meth:`DynDep.resolveImports`
     */
    private resolveImports = async (): Promise<void> => {
        Object.assign(this.ex, await ((<typeof Component>this.constructor).iPool.resolve as ModuleResolve)(
            (<typeof Component>this.constructor).requiredModules));
        await this.prepare();
    }

    /**
     * Sets the component state `ready` to `true`
     * and calls :meth:`onReady`.
     */
    private setReady = (): void => {
        this.setState({ready: true});
        this.onReady();
    }

    async iSetState(st: t.ObjectAny) {
        return await (new Promise(resolve => resolve(st))).then(
            (st) => this.setState(st));
    }

    constructor(props, context) {
        super(props, context);
        this.state = {ready: false};
        /**
         * Dynamically imported modules are put into this attribute
         * and is available to the component on :meth:`onReady`
         * and other life-cycle methods except `componentDidMount`.
         */
        this.exModules = {};
        /** A shorthand reference to the :attr:`exModules`. */
        this.ex = this.exModules;

        this.componentDidMount = this.componentDidMount.bind(this);
        this.resolveImports = this.resolveImports.bind(this);
        this.setReady = this.setReady.bind(this);
    }
}

export const URLContextType = React.createContext({});

export const DataContextType = React.createContext({});
