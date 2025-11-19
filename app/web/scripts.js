const $ = (id) => document.getElementById(id);

const dayNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
const categories = {
  10: "Music",
  24: "Entertainment",
  20: "Gaming",
  22: "People & Blogs",
  27: "Education",
  28: "Science & Technology",
  17: "Sports",
  23: "Comedy",
  1: "Film & Animation",
  25: "News & Politics",
};

const categoryBoost = {
  Music: 1.25,
  Entertainment: 1.18,
  Gaming: 1.15,
  "People & Blogs": 1.05,
  Education: 0.9,
  "Science & Technology": 0.92,
  Sports: 1.12,
  Comedy: 1.1,
  "Film & Animation": 1.15,
  "News & Politics": 0.82,
};

//-------------------------->>
// Populate dropdowns
//-------------------------->>

Object.entries(categories).forEach(([id, name]) => {
  const option = document.createElement("option");
  option.value = id;
  option.textContent = name;
  $("category").appendChild(option);
});

dayNames.forEach((name, index) => {
  const option = document.createElement("option");
  option.value = index;
  option.textContent = name;
  $("dayOfWeek").appendChild(option);
});

//-------------------------->>
// Helper: animate numbers
//-------------------------->>

function animateValue(el, start, end, duration = 600) {
  const startTime = performance.now();
  function frame(now) {
    const progress = Math.min((now - startTime) / duration, 1);
    const value = start + (end - start) * progress;
    if (typeof end === "number" && !Number.isInteger(end)) {
      el.textContent = value.toFixed(2);
    } else {
      el.textContent = Math.round(value).toLocaleString();
    }
    if (progress < 1) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}

//-------------------------->>
// Score Calculation
//-------------------------->>

function calculateEngagement() {
  const likes = Number($("likes").value || 0);
  const comments = Number($("comments").value || 0);
  const score = (likes + comments * 2) / 100;

  const engagementEl = $("engagementRate");
  const kpiEngagementEl = $("kpiEngagement");
  const prevEngagement = Number(kpiEngagementEl.textContent) || 0;

  animateValue(engagementEl, prevEngagement, score, 500);
  animateValue(kpiEngagementEl, prevEngagement, score, 500);

  return score;
}

$("likes").addEventListener("input", calculateEngagement);
$("comments").addEventListener("input", calculateEngagement);

//------------------------------------------------->>
// Generate insight text based on inputs
//------------------------------------------------->>
function buildInsight(prediction, engagement, catName, publishHour, dayOfWeek) {
  const isWeekend = dayOfWeek >= 5;
  const peakTime = publishHour >= 14 && publishHour <= 17;
  const formattedViews = prediction.toLocaleString();

  let insight = `This setup could earn around ${formattedViews} views for a ${catName} video. `;

  if (engagement >= 40) {
    insight += "Your engagement level is extremely strong — consider using this format again if it performs well. ";
  } else if (engagement >= 15) {
    insight += "Engagement looks healthy. Focus on a strong hook and clear thumbnail to fully leverage it. ";
  } else {
    insight += "Engagement is on the lower side. Try improving your title, thumbnail, and call-to-action to boost likes and comments. ";
  }

  if (peakTime && isWeekend) {
    insight += "Posting during the afternoon on a weekend gives you a powerful timing advantage.";
  } else if (peakTime) {
    insight += "Your posting time lands in a good engagement window; this will help early momentum.";
  } else if (isWeekend) {
    insight += "Weekends are generally more forgiving, but try experimenting with afternoon time slots.";
  } else {
    insight += "Consider testing afternoon slots (2–5 PM) and comparing performance across weekdays.";
  }

  return insight;
}

// Timing label ----------->>

function getTimingLabel(publishHour, dayOfWeek) {
  const isWeekend = dayOfWeek >= 5;
  const peakTime = publishHour >= 14 && publishHour <= 17;

  if (peakTime && isWeekend) return "Strong boost";
  if (peakTime) return "Moderate boost";
  if (isWeekend) return "Slight boost";
  return "Neutral";
}

// Prediction handler ---------->>

$("predictBtn").addEventListener("click", () => {
  const likes = Number($("likes").value || 0);
  const comments = Number($("comments").value || 0);
  const category = Number($("category").value);
  const publishHour = Number($("publishHour").value || 0);
  const dayOfWeek = Number($("dayOfWeek").value || 0);

  const engagement = calculateEngagement();

  const base = likes * 1.8 + comments * 12 + engagement * 20;
  const catName = categories[category] || "Unknown";
  const catBoost = categoryBoost[catName] || 1;

  const hourBoost = publishHour >= 14 && publishHour <= 17 ? 1.2 : 0.9;
  const weekendBoost = dayOfWeek >= 5 ? 1.15 : 1;

  const rawPrediction =
    base * catBoost * hourBoost * weekendBoost + Math.random() * 1500;

  const prediction = Math.max(0, Math.round(rawPrediction)); // avoid negative

  const predictedViewsEl = $("predictedViews");
  const kpiTargetEl = $("kpiTarget");
  const prevPrediction = Number(predictedViewsEl.textContent.replace(/,/g, "")) || 0;
  const prevTarget = Number(kpiTargetEl.textContent.replace(/,/g, "")) || 0;

  animateValue(predictedViewsEl, prevPrediction, prediction, 700);
  animateValue(kpiTargetEl, prevTarget, prediction, 700);

  // Range text
  const lowerRange = Math.round(prediction * 0.7).toLocaleString();
  const upperRange = Math.round(prediction * 1.3).toLocaleString();
  $("predictionRange").textContent = `Estimated range: ${lowerRange} – ${upperRange} views under similar conditions.`;

  // Summary values
  $("summaryLikes").textContent = likes.toLocaleString();
  $("summaryComments").textContent = comments.toLocaleString();
  $("summaryEngagement").textContent = engagement.toFixed(2);
  $("summaryCategory").textContent = catName;
  $("summaryHour").textContent = `${publishHour}:00`;
  $("summaryDay").textContent = dayNames[dayOfWeek] || "Unknown";

  // Timing KPI
  $("kpiTiming").textContent = getTimingLabel(publishHour, dayOfWeek);

  // Insight text
  $("insightText").textContent = buildInsight(
    prediction,
    engagement,
    catName,
    publishHour,
    dayOfWeek
  );
});
