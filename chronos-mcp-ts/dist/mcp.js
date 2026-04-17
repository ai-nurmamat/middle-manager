"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.MCPGateway = void 0;
const graph_1 = require("./graph");
const sleep_1 = require("./sleep");
class MCPGateway {
    constructor() {
        this.extractor = null;
        this.graph = new graph_1.UniversalHypergraph();
        this.consolidator = new sleep_1.SleepConsolidator(this.graph);
    }
    async injectKnowledge(text, sourceId, publishDateStr) {
        if (!this.extractor) {
            throw new Error('Extractor not initialized');
        }
        const dt = new Date(publishDateStr);
        await this.extractor.extractToGraph(text, sourceId, dt, this.graph);
        return { status: 'success', message: `Knowledge injected from ${sourceId}` };
    }
    triggerSleep() {
        this.consolidator.sleepAndReflect();
        return { status: 'success', message: 'Graph ontology consolidated.' };
    }
    queryGraph(params) {
        const res = this.graph.query(params);
        return res.map(t => ({
            S: t.subject,
            P: t.predicate,
            O: `${t.object}${t.unit || ''}`,
            Time: t.time.toISOString().split('T')[0],
            Source: t.evidence ? t.evidence.sourceId : 'N/A'
        }));
    }
}
exports.MCPGateway = MCPGateway;
