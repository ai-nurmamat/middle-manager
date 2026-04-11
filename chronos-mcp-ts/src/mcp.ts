import { UniversalHypergraph } from './graph';
import { UniversalExtractor } from './llm';
import { SleepConsolidator } from './sleep';

export class MCPGateway {
  public graph: UniversalHypergraph;
  public extractor: UniversalExtractor | null = null;
  private consolidator: SleepConsolidator;

  constructor() {
    this.graph = new UniversalHypergraph();
    this.consolidator = new SleepConsolidator(this.graph);
  }

  async injectKnowledge(text: string, sourceId: string, publishDateStr: string) {
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

  queryGraph(params: { subject?: string; predicate?: string; object?: string }) {
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
