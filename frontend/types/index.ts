export interface PredictionResult {
  prediction: string;
  probabilities: {
    Dropout: number;
    Enrolled: number;
    Graduate: number;
  };
  dropout_probability: number;
  risk_level: string;
  risk_color: string;
  recommendation: string;
  insights: string[];
  timestamp: string;
}

export interface ModelMetadata {
  model_name: string;
  trained_date: string;
  metrics: {
    accuracy: number;
    f1_macro: number;
    dropout_recall: number;
  };
}
