import { UniversalHypergraph } from './graph';
export declare class SleepConsolidator {
    private graph;
    private entityAliases;
    private predicateAliases;
    constructor(graph: UniversalHypergraph);
    sleepAndReflect(): void;
}
