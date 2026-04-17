"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.UniversalHypergraph = void 0;
const uuid_1 = require("uuid");
/**
 * Universal 4D Hypergraph Memory Engine.
 *
 * A pure in-memory O(1) indexing engine that natively supports Temporal Knowledge Graphs.
 * It indexes tuples by Subject, Predicate, and Object to allow instant multidimensional queries.
 */
class UniversalHypergraph {
    constructor() {
        this.tuples = {};
        this.sIndex = {};
        this.pIndex = {};
        this.oIndex = {};
    }
    /**
     * Insert a FourDTuple into the hypergraph and update indexes.
     *
     * @param tup - The tuple to insert.
     * @returns The unique ID of the inserted tuple.
     */
    insert(tup) {
        if (!tup.id) {
            tup.id = `tup_${(0, uuid_1.v4)().substring(0, 8)}`;
        }
        this.tuples[tup.id] = tup;
        if (!this.sIndex[tup.subject])
            this.sIndex[tup.subject] = [];
        this.sIndex[tup.subject].push(tup.id);
        if (!this.pIndex[tup.predicate])
            this.pIndex[tup.predicate] = [];
        this.pIndex[tup.predicate].push(tup.id);
        if (!this.oIndex[tup.object])
            this.oIndex[tup.object] = [];
        this.oIndex[tup.object].push(tup.id);
        return tup.id;
    }
    /**
     * Query the Universal Hypergraph across any combination of dimensions.
     *
     * @param params - The query filters.
     * @returns A chronologically sorted array of matching tuples.
     */
    query(params) {
        let candidates = null;
        const intersect = (index, key) => {
            const currentSet = new Set(index[key] || []);
            if (candidates === null) {
                candidates = currentSet;
            }
            else {
                candidates = new Set([...candidates].filter((x) => currentSet.has(x)));
            }
        };
        if (params.subject)
            intersect(this.sIndex, params.subject);
        if (params.predicate)
            intersect(this.pIndex, params.predicate);
        if (params.object)
            intersect(this.oIndex, params.object);
        if (candidates === null) {
            candidates = new Set(Object.keys(this.tuples));
        }
        const results = [];
        for (const cid of candidates) {
            const t = this.tuples[cid];
            if (params.startTime && t.time < params.startTime)
                continue;
            if (params.endTime && t.time > params.endTime)
                continue;
            results.push(t);
        }
        return results.sort((a, b) => a.time.getTime() - b.time.getTime());
    }
}
exports.UniversalHypergraph = UniversalHypergraph;
