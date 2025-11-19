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

//================================================>
// Populate dropdowns
//================================================>
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


function calculateEngagement() {
  const likes = Number($("likes").value || 0);
  const comments = Number($("comments").value || 0);
  const score = (likes + comments * 2) / 100;

  $("engagementRate").textContent = score.toFixed(2);
  return score;
}

$("likes").addEventListener("input", calculateEngagement);
$("comments").addEventListener("input", calculateEngagement);

//================================================>
//  Predict Button Click Handler
//================================================>

$("predictBtn").addEventListener("click", () => {
  const likes = Number($("likes").value);
  const comments = Number($("comments").value);
  const category = Number($("category").value);
  const publishHour = Number($("publishHour").value);
  const dayOfWeek = Number($("dayOfWeek").value);

  const engagement = calculateEngagement();

  const base = likes * 1.8 + comments * 12 + engagement * 20;

  const catName = categories[category];
  const catBoost = categoryBoost[catName] || 1;

  const hourBoost = publishHour >= 14 && publishHour <= 17 ? 1.2 : 0.9;
  const weekendBoost = dayOfWeek >= 5 ? 1.15 : 1;

  const prediction = Math.round(
    base * catBoost * hourBoost * weekendBoost + Math.random() * 2000
  );

  $("predictedViews").textContent = prediction.toLocaleString();
  $("predictionResult").classList.remove("hidden");

  $("summaryLikes").textContent = likes.toLocaleString();
  $("summaryComments").textContent = comments.toLocaleString();
  $("summaryEngagement").textContent = engagement.toFixed(2);
  $("summaryCategory").textContent = catName;
  $("summaryHour").textContent = publishHour + ":00";
  $("summaryDay").textContent = dayNames[dayOfWeek];

  $("summarySection").classList.remove("hidden");
});
