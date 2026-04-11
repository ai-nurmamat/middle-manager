import { UniversalHypergraph, FourDTuple } from '../src/graph';
import { SleepConsolidator } from '../src/sleep';

describe('UniversalHypergraph Core', () => {
  it('should insert and query tuples successfully', () => {
    const graph = new UniversalHypergraph();
    
    const tup1: FourDTuple = {
      id: '',
      subject: 'CATL',
      predicate: '毛利率',
      object: '28.5',
      time: new Date('2023-09-30')
    };
    
    const tup2: FourDTuple = {
      id: '',
      subject: 'CATL',
      predicate: '投资',
      object: '固态电池',
      time: new Date('2023-10-15')
    };
    
    graph.insert(tup1);
    graph.insert(tup2);
    
    const res1 = graph.query({ subject: 'CATL' });
    expect(res1.length).toBe(2);
    
    const res2 = graph.query({ predicate: '投资' });
    expect(res2.length).toBe(1);
    expect(res2[0].object).toBe('固态电池');
    
    const res3 = graph.query({ subject: 'CATL', predicate: '毛利率' });
    expect(res3.length).toBe(1);
    expect(res3[0].object).toBe('28.5');
  });

  it('should consolidate noisy aliases during sleep', () => {
    const graph = new UniversalHypergraph();
    
    const tup1: FourDTuple = {
      id: '',
      subject: '宁王',
      predicate: '毛利',
      object: '27.0',
      time: new Date('2022-09-30')
    };
    
    graph.insert(tup1);
    
    let resBefore = graph.query({ subject: '宁王', predicate: '毛利' });
    expect(resBefore.length).toBe(1);
    
    const consolidator = new SleepConsolidator(graph);
    consolidator.sleepAndReflect();
    
    let resAfter = graph.query({ subject: '宁德时代', predicate: '毛利率' });
    expect(resAfter.length).toBe(1);
    expect(resAfter[0].object).toBe('27.0');
    
    let oldAliasQuery = graph.query({ subject: '宁王' });
    expect(oldAliasQuery.length).toBe(0);
  });
});
