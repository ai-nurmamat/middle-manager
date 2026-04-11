import { v4 as uuidv4 } from 'uuid';

export interface SourceEvidence {
  sourceId: string;
  textSnippet: string;
  timestamp: Date;
}

export interface FourDTuple {
  id: string;
  subject: string;
  predicate: string;
  object: string;
  time: Date;
  unit?: string;
  evidence?: SourceEvidence;
}

export class UniversalHypergraph {
  public tuples: Record<string, FourDTuple> = {};
  private sIndex: Record<string, string[]> = {};
  private pIndex: Record<string, string[]> = {};
  private oIndex: Record<string, string[]> = {};

  insert(tup: FourDTuple): string {
    if (!tup.id) {
      tup.id = `tup_${uuidv4().substring(0, 8)}`;
    }
    this.tuples[tup.id] = tup;
    
    if (!this.sIndex[tup.subject]) this.sIndex[tup.subject] = [];
    this.sIndex[tup.subject].push(tup.id);
    
    if (!this.pIndex[tup.predicate]) this.pIndex[tup.predicate] = [];
    this.pIndex[tup.predicate].push(tup.id);
    
    if (!this.oIndex[tup.object]) this.oIndex[tup.object] = [];
    this.oIndex[tup.object].push(tup.id);
    
    return tup.id;
  }

  query(params: {
    subject?: string;
    predicate?: string;
    object?: string;
    startTime?: Date;
    endTime?: Date;
  }): FourDTuple[] {
    let candidates: Set<string> | null = null;

    const intersect = (index: Record<string, string[]>, key: string) => {
      const currentSet = new Set(index[key] || []);
      if (candidates === null) {
        candidates = currentSet;
      } else {
        candidates = new Set([...candidates].filter(x => currentSet.has(x)));
      }
    };

    if (params.subject) intersect(this.sIndex, params.subject);
    if (params.predicate) intersect(this.pIndex, params.predicate);
    if (params.object) intersect(this.oIndex, params.object);

    if (candidates === null) {
      candidates = new Set(Object.keys(this.tuples));
    }

    const results: FourDTuple[] = [];
    for (const cid of candidates) {
      const t = this.tuples[cid];
      if (params.startTime && t.time < params.startTime) continue;
      if (params.endTime && t.time > params.endTime) continue;
      results.push(t);
    }

    return results.sort((a, b) => a.time.getTime() - b.time.getTime());
  }
}
