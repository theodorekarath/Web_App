const canvas = document.querySelector("#drawing-canvas");
const context = canvas.getContext("2d");
const predictButton = document.querySelector("#predict-button");
const clearButton = document.querySelector("#clear-button");
const result = document.querySelector("#result");
const BRUSH_RADIUS = 15;
let isDrawing = false;
let hasInk = false;

context.strokeStyle = "white";
context.lineWidth = BRUSH_RADIUS * 2;
context.lineCap = "round";
context.lineJoin = "round";

function clearCanvas() {
  context.fillStyle = "black";
  context.fillRect(0, 0, canvas.width, canvas.height);
  hasInk = false;
  result.textContent = "";
}
function pointFromEvent(event) {
  const bounds = canvas.getBoundingClientRect();
  return { x: (event.clientX - bounds.left) * canvas.width / bounds.width, y: (event.clientY - bounds.top) * canvas.height / bounds.height };
}
function drawDot(point) {
  context.fillStyle = "white";
  context.beginPath();
  context.arc(point.x, point.y, BRUSH_RADIUS, 0, Math.PI * 2);
  context.fill();
}
function startDrawing(event) {
  isDrawing = true;
  hasInk = true;
  const point = pointFromEvent(event);
  drawDot(point);
  context.beginPath();
  context.moveTo(point.x, point.y);
  canvas.setPointerCapture(event.pointerId);
}
function continueDrawing(event) {
  if (!isDrawing) return;
  const point = pointFromEvent(event);
  context.lineTo(point.x, point.y);
  context.stroke();
  context.beginPath();
  context.moveTo(point.x, point.y);
}
function stopDrawing() { isDrawing = false; }

canvas.addEventListener("pointerdown", startDrawing);
canvas.addEventListener("pointermove", continueDrawing);
canvas.addEventListener("pointerup", stopDrawing);
canvas.addEventListener("pointercancel", stopDrawing);
clearButton.addEventListener("click", clearCanvas);
predictButton.addEventListener("click", async () => {
  if (!hasInk) { result.textContent = "Draw a digit before predicting."; return; }
  predictButton.disabled = true;
  result.textContent = "Predicting...";
  try {
    const response = await fetch("/predict", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ image: canvas.toDataURL("image/png") }) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Prediction failed.");
    result.textContent = `Prediction: ${data.digit}  Confidence: ${data.confidence.toFixed(2)}%`;
    if (!data.confident) result.textContent += " (Not confident enough.)";
  } catch (error) { result.textContent = error.message; }
  finally { predictButton.disabled = false; }
});
clearCanvas();
