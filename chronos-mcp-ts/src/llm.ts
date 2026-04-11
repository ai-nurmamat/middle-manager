import { OpenAI } from 'openai';
import { UniversalHypergraph, FourDTuple, SourceEvidence } from './graph';
import { v4 as uuidv4 } from 'uuid';

export class UniversalExtractor {
  private client: OpenAI;
  private model: string;

  constructor(apiKey: string, baseUrl: string, model: string) {
    this.client = new OpenAI({ apiKey, baseURL: baseUrl });
    this.model = model;
  }

  async extractToGraph(
    text: string,
    sourceId: string,
    publishDate: Date,
    graph: UniversalHypergraph
  ) {
    const prompt = `
    你是一个顶级的时序知识图谱构建专家。
    你的任务是将下方文本中所有具有【商业价值、分析价值】的信息，彻底转化为 4D Tuples 数组。
    
    【四维元组规则 (S, P, O, T)】：
    1. S (主体): 公司名、产品名、人名等实体。如 "宁德时代"
    2. P (谓语): 属性名、关系名、动作名。无需预先定义！你自由发挥。如 "毛利率", "投资", "市盈率", "竞争对手"
    3. O (客体): 数值、字符串、或另一个实体。如 "28.5", "固态电池", "比亚迪"
    4. U (单位): 如果 Object 是数值，提炼出单位，如 "%", "亿元"。否则为空。
    5. T (时间): 该事实成立或发生的时间 (YYYY-MM-DD)。
    6. Snippet (片段): 证明该元组的一句原文。
    
    文本时间基准：该文本发布于 ${publishDate.toISOString().split('T')[0]}。
    
    【严格要求】：只返回合法的 JSON 数组，无需任何解释。
    格式示例：
    [
      {"S": "宁德时代", "P": "毛利率", "O": "28.5", "U": "%", "T": "2023-09-30", "Snippet": "宁德时代毛利率为28.5%"},
      {"S": "宁德时代", "P": "研发", "O": "固态电池", "U": "", "T": "2023-10-15", "Snippet": "开始研发固态电池"}
    ]
    `;

    try {
      const response = await this.client.chat.completions.create({
        model: this.model,
        messages: [
          { role: 'system', content: prompt },
          { role: 'user', content: text }
        ],
        response_format: { type: 'json_object' }
      });

      const rawJson = response.choices[0].message.content || '{}';
      let data = JSON.parse(rawJson);
      let tuples: any[] = [];

      if (Array.isArray(data)) {
        tuples = data;
      } else if (data.tuples) {
        tuples = data.tuples;
      } else {
        const values = Object.values(data);
        if (values.length > 0 && Array.isArray(values[0])) {
          tuples = values[0];
        }
      }

      for (const t of tuples) {
        const evidence: SourceEvidence = {
          sourceId,
          textSnippet: t.Snippet || '',
          timestamp: publishDate
        };

        const timeStr = t.T || publishDate.toISOString().split('T')[0];
        let dt = publishDate;
        try {
          dt = new Date(timeStr.substring(0, 10));
        } catch (e) {
          // fallback to publishDate
        }

        const tup: FourDTuple = {
          id: `tup_${uuidv4().substring(0, 8)}`,
          subject: t.S || '',
          predicate: t.P || '',
          object: String(t.O || ''),
          time: dt,
          unit: t.U || '',
          evidence
        };

        graph.insert(tup);
      }
      console.log(`✅ Extracted ${tuples.length} tuples from ${sourceId}.`);
    } catch (error) {
      console.error(`❌ Extraction failed:`, error);
    }
  }
}
