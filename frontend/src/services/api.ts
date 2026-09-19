import {
  WasteInput,
  AssessmentResult,
  AssessmentRecord,
  RuleResponse,
  MaterialResponse,
  StatisticsResponse,
  MLModelStatus,
} from '../types';

const API_BASE = 'http://127.0.0.1:8000/api';

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorMsg = `Server returned ${res.status}: ${res.statusText}`;
    try {
      const errJson = await res.json();
      if (errJson.detail) {
        errorMsg = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail);
      }
    } catch {
      // ignore
    }
    throw new Error(errorMsg);
  }
  return res.json();
}

export const api = {
  async analyzeWaste(input: WasteInput): Promise<AssessmentResult> {
    const res = await fetch(`${API_BASE}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input),
    });
    return handleResponse<AssessmentResult>(res);
  },

  async getAssessments(material?: string, pathway?: string, search?: string): Promise<AssessmentRecord[]> {
    const params = new URLSearchParams();
    if (material) params.append('material', material);
    if (pathway) params.append('pathway', pathway);
    if (search) params.append('search', search);

    const qs = params.toString() ? `?${params.toString()}` : '';
    const res = await fetch(`${API_BASE}/assessments${qs}`);
    return handleResponse<AssessmentRecord[]>(res);
  },

  async getAssessment(id: number): Promise<AssessmentResult> {
    const res = await fetch(`${API_BASE}/assessments/${id}`);
    return handleResponse<AssessmentResult>(res);
  },

  async deleteAssessment(id: number): Promise<{ status: string; message: string }> {
    const res = await fetch(`${API_BASE}/assessments/${id}`, {
      method: 'DELETE',
    });
    return handleResponse<{ status: string; message: string }>(res);
  },

  async getRules(material?: string, pathway?: string): Promise<RuleResponse[]> {
    const params = new URLSearchParams();
    if (material) params.append('material', material);
    if (pathway) params.append('pathway', pathway);

    const qs = params.toString() ? `?${params.toString()}` : '';
    const res = await fetch(`${API_BASE}/rules${qs}`);
    return handleResponse<RuleResponse[]>(res);
  },

  async getRule(ruleId: string): Promise<RuleResponse> {
    const res = await fetch(`${API_BASE}/rules/${ruleId}`);
    return handleResponse<RuleResponse>(res);
  },

  async getMaterials(): Promise<MaterialResponse[]> {
    const res = await fetch(`${API_BASE}/materials`);
    return handleResponse<MaterialResponse[]>(res);
  },

  async getMaterial(name: string): Promise<MaterialResponse> {
    const res = await fetch(`${API_BASE}/materials/${encodeURIComponent(name)}`);
    return handleResponse<MaterialResponse>(res);
  },

  async getStatistics(): Promise<StatisticsResponse> {
    const res = await fetch(`${API_BASE}/statistics`);
    return handleResponse<StatisticsResponse>(res);
  },

  async getMLStatus(): Promise<MLModelStatus> {
    const res = await fetch(`${API_BASE}/ml/status`);
    return handleResponse<MLModelStatus>(res);
  },

  async checkHealth(): Promise<{ status: string; service: string; mode: string }> {
    const res = await fetch(`${API_BASE}/health`);
    return handleResponse<{ status: string; service: string; mode: string }>(res);
  },
};
