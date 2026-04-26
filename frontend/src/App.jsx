import { useState } from "react";
import "./App.css";

export default function App() {
  const [data, setData] = useState(null);
  const [resumeText, setResumeText] = useState("");
  const [jdText, setJdText] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [jdFile, setJdFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setData(null);

    const formData = new FormData();
    if (resumeText) formData.append("resume_text", resumeText);
    if (jdText) formData.append("jd_text", jdText);
    if (resumeFile) formData.append("resume_file", resumeFile);
    if (jdFile) formData.append("jd_file", jdFile);

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData,
      });

      const result = await res.json();

      if (result.success && result.data) {
        const safe = {
          match_score: result.data.match_score || "0%",
          summary: result.data.summary || "",
          decision: result.data.decision || "",
          resume_skills: result.data.resume_skills || [],
          jd_skills: result.data.jd_skills || [],
          skill_scores: result.data.skill_scores || {},
          gaps: result.data.gaps || [],
          gap_priority: result.data.gap_priority || {},
          questions: result.data.questions || {},
          learning_plan: result.data.learning_plan || []
        };

        setData(safe);
        setResumeText(result.resume_text || "");
        setJdText(result.jd_text || "");
      } else {
        setData({ error: result.error });
      }

    } catch {
      setData({ error: "Backend error" });
    }

    setLoading(false);
  };

  return (
    <div className="app">

      <h1 className="title">AI Skill Assessment Agent</h1>

      <div className="input-section">
        <div className="card">
          <h3>Resume</h3>
          <textarea value={resumeText} onChange={e => setResumeText(e.target.value)} />
          <input type="file" onChange={e => setResumeFile(e.target.files[0])} />
        </div>

        <div className="card">
          <h3>Job Description</h3>
          <textarea value={jdText} onChange={e => setJdText(e.target.value)} />
          <input type="file" onChange={e => setJdFile(e.target.files[0])} />
        </div>
      </div>

      <button className="btn" onClick={handleSubmit}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {data && (
        <div className="result">

          <h2 className="match">Match Score: {data.match_score}</h2>
          <div className="progress">
            <div className="bar" style={{ width: data.match_score }}></div>
          </div>

          <p className="summary">{data.summary}</p>
          <p className="decision">{data.decision}</p>

          <Section title="Resume Skills" items={data.resume_skills} />
          <Section title="JD Skills" items={data.jd_skills} />

          <h2>Skill Scores</h2>
          {Object.entries(data.skill_scores).slice(0, 10).map(([k,v]) => (
            <div key={k} className="score">
              <span>{k}</span>
              <span>{v}</span>
            </div>
          ))}

          <h2>Skill Gaps</h2>
          {data.gaps.map((g,i)=>(
            <div key={i}>{g} ({data.gap_priority[g]})</div>
          ))}

          <h2>Interview Questions</h2>
          {Object.entries(data.questions).map(([k,qs])=>(
            <div key={k}>
              <b>{k}</b>
              <ul>{qs.map((q,i)=><li key={i}>{q}</li>)}</ul>
            </div>
          ))}

          <h2>Learning Plan</h2>
          {data.learning_plan.map((item,i)=>(
            <div key={i} className="card">
              <h3>{item.skill}</h3>
              <p><b>Why:</b> {item.reason}</p>
              <p><b>Time:</b> {item.time}</p>
              <ul>{item.resources.map((r,j)=><li key={j}>{r}</li>)}</ul>
            </div>
          ))}

        </div>
      )}
    </div>
  );
}

function Section({ title, items }) {
  return (
    <>
      <h2>{title}</h2>
      <div className="tags">
        {items.map((i,idx)=>
          <span key={idx} className="tag">{i}</span>
        )}
      </div>
    </>
  );
}