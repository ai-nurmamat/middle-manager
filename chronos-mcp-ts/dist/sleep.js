"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SleepConsolidator = void 0;
class SleepConsolidator {
    constructor(graph) {
        this.entityAliases = {
            'CATL': '宁德时代',
            '宁王': '宁德时代',
            '比亚迪': '比亚迪',
            '全固态电池': '固态电池'
        };
        this.predicateAliases = {
            '毛利': '毛利率',
            '储能毛利': '储能毛利率',
            '重仓': '投资',
            '竞品': '竞争对手'
        };
        this.graph = graph;
    }
    sleepAndReflect() {
        console.log('\n💤 [Consolidation] The engine goes to sleep... reflecting on memory.');
        let updatedCount = 0;
        for (const [tId, tup] of Object.entries(this.graph.tuples)) {
            if (this.entityAliases[tup.subject]) {
                const normSub = this.entityAliases[tup.subject];
                if (tup.subject !== normSub) {
                    const index = this.graph.sIndex[tup.subject];
                    index.splice(index.indexOf(tId), 1);
                    tup.subject = normSub;
                    if (!this.graph.sIndex[normSub])
                        this.graph.sIndex[normSub] = [];
                    this.graph.sIndex[normSub].push(tId);
                    updatedCount++;
                }
            }
            if (this.predicateAliases[tup.predicate]) {
                const normPred = this.predicateAliases[tup.predicate];
                if (tup.predicate !== normPred) {
                    const index = this.graph.pIndex[tup.predicate];
                    index.splice(index.indexOf(tId), 1);
                    tup.predicate = normPred;
                    if (!this.graph.pIndex[normPred])
                        this.graph.pIndex[normPred] = [];
                    this.graph.pIndex[normPred].push(tId);
                    updatedCount++;
                }
            }
            if (this.entityAliases[tup.object]) {
                const normObj = this.entityAliases[tup.object];
                if (tup.object !== normObj) {
                    const index = this.graph.oIndex[tup.object];
                    index.splice(index.indexOf(tId), 1);
                    tup.object = normObj;
                    if (!this.graph.oIndex[normObj])
                        this.graph.oIndex[normObj] = [];
                    this.graph.oIndex[normObj].push(tId);
                    updatedCount++;
                }
            }
        }
        console.log(`✨ [Consolidation] Woke up! Consolidated ${updatedCount} noisy aliases into a unified schema.\n`);
    }
}
exports.SleepConsolidator = SleepConsolidator;
