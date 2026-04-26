export async function analyze(resume, job_description) {
  const res = await fetch("http://localhost:8000/analyze", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ resume, job_description })
  });
  return res.json();
}