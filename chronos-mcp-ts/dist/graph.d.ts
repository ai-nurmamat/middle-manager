/**
 * Evidence to trace back the origin of a data point, eliminating AI hallucinations.
 */
export interface SourceEvidence {
    /** Unique identifier of the source document/report */
    sourceId: string;
    /** The original text snippet from which the data was extracted */
    textSnippet: string;
    /** The publication or occurrence time of the source */
    timestamp: Date;
}
/**
 * The Universal 4D Tuple: S-P-O-T
 * (Subject, Predicate, Object, Time)
 *
 * This disruptive model breaks the boundaries between traditional property graphs
 * and time-series databases by representing everything as a temporal edge.
 */
export interface FourDTuple {
    /** Unique identifier of the tuple */
    id: string;
    /** The subject entity, e.g., 'CATL', 'Apple' */
    subject: string;
    /** The relation or property, e.g., 'gross margin', 'invests_in' */
    predicate: string;
    /** The object entity or value, e.g., '28.5', 'Solid State Battery' */
    object: string;
    /** The exact time when this fact is valid or occurred */
    time: Date;
    /** The unit if the object is a numeric value, e.g., '%', 'USD' */
    unit?: string;
    /** Source evidence to guarantee traceability */
    evidence?: SourceEvidence;
}
/**
 * Universal 4D Hypergraph Memory Engine.
 *
 * A pure in-memory O(1) indexing engine that natively supports Temporal Knowledge Graphs.
 * It indexes tuples by Subject, Predicate, and Object to allow instant multidimensional queries.
 */
export declare class UniversalHypergraph {
    tuples: Record<string, FourDTuple>;
    private sIndex;
    private pIndex;
    private oIndex;
    /**
     * Insert a FourDTuple into the hypergraph and update indexes.
     *
     * @param tup - The tuple to insert.
     * @returns The unique ID of the inserted tuple.
     */
    insert(tup: FourDTuple): string;
    /**
     * Query the Universal Hypergraph across any combination of dimensions.
     *
     * @param params - The query filters.
     * @returns A chronologically sorted array of matching tuples.
     */
    query(params: {
        subject?: string;
        predicate?: string;
        object?: string;
        startTime?: Date;
        endTime?: Date;
    }): FourDTuple[];
}
