import type { FlowsheetData, ModelRevisionData, SimulatorObjectEdge } from '../types/flowsheet';

/**
 * Normalize flowsheet data to handle both old and new formats
 */
export function normalizeFlowsheetData(data: any): FlowsheetData | null {
  if (!data) return null;

  // Check if this is a ModelRevisionData structure
  if (data.modelRevisionExternalId && data.flowsheets && Array.isArray(data.flowsheets)) {
    const modelRevision = data as ModelRevisionData;
    // Return the first flowsheet if available
    return modelRevision.flowsheets.length > 0 ? modelRevision.flowsheets[0] : null;
  }

  // Check if this is already a FlowsheetData structure
  if (data.simulatorObjectNodes || data.simulatorObjectEdges) {
    return data as FlowsheetData;
  }

  // Legacy format check
  if (data.items && Array.isArray(data.items) && data.items.length > 0) {
    // Handle old format: { items: [{ flowsheet: {...} }] }
    const firstItem = data.items[0];
    if (firstItem.flowsheet) {
      return firstItem.flowsheet as FlowsheetData;
    }
    if (firstItem.flowsheets && Array.isArray(firstItem.flowsheets)) {
      return firstItem.flowsheets[0] as FlowsheetData;
    }
  }

  return null;
}

/**
 * Get source and target IDs from edge, handling both old and new formats
 */
export function getEdgeSourceTarget(edge: SimulatorObjectEdge): { sourceId: string; targetId: string } | null {
  // Try new format first
  if (edge.sourceId && edge.targetId) {
    return { sourceId: edge.sourceId, targetId: edge.targetId };
  }

  // Fall back to legacy format
  if (edge.source && edge.target) {
    return { sourceId: edge.source, targetId: edge.target };
  }

  return null;
}

/**
 * Format property value for display
 */
export function formatPropertyValue(value: any): string {
  if (value === null || value === undefined) return '-';
  
  if (Array.isArray(value)) {
    // Format array values
    if (value.length === 0) return '[]';
    if (value.length <= 3) {
      return `[${value.map(v => typeof v === 'number' ? formatNumber(v) : v).join(', ')}]`;
    }
    return `[${formatNumber(value[0])}, ..., ${formatNumber(value[value.length - 1])}] (${value.length} items)`;
  }
  
  if (typeof value === 'number') {
    return formatNumber(value);
  }
  
  return value.toString();
}

/**
 * Format a number for display
 */
function formatNumber(value: number): string {
  if (value === 0) return '0';
  if (Math.abs(value) < 0.0001 || Math.abs(value) > 1000000) {
    return value.toExponential(4);
  }
  if (value % 1 === 0) {
    return value.toString();
  }
  return value.toFixed(4);
}

/**
 * Get unit display string from property unit
 */
export function getUnitDisplay(unit: any): string {
  if (!unit) return '';
  
  if (typeof unit === 'string') {
    return unit;
  }
  
  if (typeof unit === 'object' && unit.name) {
    return unit.name;
  }
  
  return '';
}

/**
 * Get unit quantity from property unit
 */
export function getUnitQuantity(unit: any): string | undefined {
  if (typeof unit === 'object' && unit.quantity) {
    return unit.quantity;
  }
  return undefined;
}

