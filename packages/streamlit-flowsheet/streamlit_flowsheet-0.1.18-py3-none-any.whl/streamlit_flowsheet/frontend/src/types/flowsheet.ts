export interface Position {
  x: number;
  y: number;
}

export interface GraphicalObject {
  position: Position;
  height?: number;
  width?: number;
  angle?: number;
  active?: boolean;
  scaleX?: number;
  scaleY?: number;
}

// Support multiple reference object formats
export interface ReferenceObject {
  // Legacy format
  address?: string;
  
  // iise.json format
  link?: string;
  components?: string; // Pipe-separated component names for arrays
  
  // dwsim.json format
  objectName?: string;
  objectType?: string;
  objectProperty?: string;
}

export interface PropertyUnit {
  name: string;
  quantity?: string;
}

export interface Property {
  name: string;
  referenceObject?: ReferenceObject;
  valueType?: string;
  value?: number | string | number[] | string[]; // Support arrays
  unit?: PropertyUnit | string; // Support both object and legacy string format
  readOnly?: boolean;
  category?: string; // For grouping properties
}

export interface SimulatorObjectNode {
  id: string;
  name: string;
  type: string;
  graphicalObject?: GraphicalObject;
  properties?: Property[];
}

export interface SimulatorObjectEdge {
  id: string;
  name?: string;
  
  // New format
  sourceId?: string;
  targetId?: string;
  connectionType?: string;
  
  // Legacy format (for backward compatibility)
  source?: string;
  target?: string;
  sourcePort?: string;
  targetPort?: string;
}

export interface Thermodynamics {
  propertyPackages?: string[];
  components?: string[];
}

export interface FlowsheetData {
  simulatorObjectNodes?: SimulatorObjectNode[];
  simulatorObjectEdges?: SimulatorObjectEdge[];
  thermodynamics?: Thermodynamics;
}

// Top-level model revision structure
export interface ModelRevisionData {
  modelRevisionExternalId: string;
  flowsheets: FlowsheetData[];
  dataSetId?: number;
  createdTime?: number;
  lastUpdatedTime?: number;
}