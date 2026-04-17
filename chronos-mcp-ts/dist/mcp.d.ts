import { UniversalHypergraph } from './graph';
import { UniversalExtractor } from './llm';
export declare class MCPGateway {
    graph: UniversalHypergraph;
    extractor: UniversalExtractor | null;
    private consolidator;
    constructor();
    injectKnowledge(text: string, sourceId: string, publishDateStr: string): Promise<{
        status: string;
        message: string;
    }>;
    triggerSleep(): {
        status: string;
        message: string;
    };
    queryGraph(params: {
        subject?: string;
        predicate?: string;
        object?: string;
    }): {
        S: string;
        P: string;
        O: string;
        Time: string;
        Source: string;
    }[];
}
