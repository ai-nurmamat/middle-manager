import { UniversalHypergraph } from './graph';
export declare class UniversalExtractor {
    private client;
    private model;
    constructor(apiKey: string, baseUrl: string, model: string);
    extractToGraph(text: string, sourceId: string, publishDate: Date, graph: UniversalHypergraph): Promise<void>;
}
