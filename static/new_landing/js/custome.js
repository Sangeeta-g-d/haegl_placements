// Get the id passed from the view
function education() {
  var container = document.getElementById('container2');
  container.classList.toggle('hidden');
}

function addNewEducation() {
  var container = document.getElementById('container2');
  var educationCount = container.getElementsByClassName('education-section').length + 1;
  var newEducation = document.createElement('div');
  newEducation.classList.add('education-section');

  var header = document.createElement('div');
  header.classList.add('education-header');
  header.onclick = function () { toggleEducation(this) };
  header.innerHTML = '<i class="fas fa-chevron-down"></i><p><b><span id="educationTitle' + educationCount + '">Education ' + educationCount + '</span></b></p>' +
                     '<i class="fas fa-trash-alt" onclick="deleteEducation(' + educationCount + ')"></i>'; // Delete icon added here

  var content = document.createElement('div');
  content.classList.add('education-content');

  var formId = 'education' + educationCount;
  var degreeInputId = 'degreeInput' + educationCount;
  var institutionInputId = 'institution' + educationCount;
  var cityInputId = 'city' + educationCount;
  var fromInputId = 'degreeFromInput' + educationCount;
  var toInputId = 'to' + educationCount;

  content.innerHTML = '<form id="' + formId + '">' +
    '<div class="form-group">' +
    '<input type="text" id="' + institutionInputId + '" class="form-control" placeholder="Institution Name" name="' + institutionInputId + '" style="height: 30px;" oninput="updateDisplay(' + educationCount + ')">' +
    '</div>' +
    '<div class="form-group">' +
    '<input type="text" id="' + degreeInputId + '" class="form-control" placeholder="Degree" name="' + degreeInputId + '" style="height: 30px;" oninput="updateDisplay(' + educationCount + ')">' +
    '</div>' +
    '<div class="form-group">' + 
    '<input type="text" id="' + cityInputId + '" class="form-control" placeholder="City" name="' + cityInputId + '" style="height: 30px;" oninput="updateDisplay(' + educationCount + ')">' +
    '</div>' +
    '<div class="form-group">' +
    '<label for="' + fromInputId + '" style="margin-right: 10px;">From:</label>' +
    '<input type="month" id="' + fromInputId + '" name="' + fromInputId + '" class="form-control" style="height: 35px;" onchange="updateDisplay(' + educationCount + ')">' +
    '</div>' +
    '<div class="form-group">' +
    '<label for="' + toInputId + '" style="margin-right: 10px;">To:</label>' +
    '<input type="month" id="' + toInputId + '" class="form-control" name="' + toInputId + '" style="height: 35px;" onchange="updateDisplay(' + educationCount + ')">' +
    '</div>' +
    '</form>';

  newEducation.appendChild(header);
  newEducation.appendChild(content);
  container.insertBefore(newEducation, container.lastElementChild);

  var displayDiv = generateDisplayDiv(educationCount);
  var educationContainer = document.getElementById('educationContainer');
  educationContainer.appendChild(displayDiv);

  saveEducation();
}
function generateDisplayDiv(educationCount) {
  var displayDiv = document.createElement('div');
  displayDiv.classList.add('education');
  displayDiv.style.marginTop = "30px";

  var institution = 'Copenhagen School of Design and Technology';
  var city = 'City'; // Default city value
  // Here you can add logic to get the actual city value if needed

  displayDiv.innerHTML = 
    '<div>' +
    '<p style="font-size: 14px;line-height: 8px;">' +
    '<span id="displayDegree' + educationCount + '"><b>Bachelor of Engineering </b></span><br>' +
    '</p>' +
    '<p style="font-size: 14px;line-height: 4px;">' +
    '<span id="displayDegreeFrom' + educationCount + '"> <b>2015 </b> </span> | <span id="displayDegreeTo' + educationCount + '"> <b>2017</b> </span>' +
    '</p>' +
    '<p id="displayCollege' + educationCount + '">' +
    institution + ' - <span id="displayCity' + educationCount + '">' + city + '</span>' +
    '</p>' +
    '</div>';

  return displayDiv;
}

function deleteEducation(educationCount) {
  console.log("vidya")
  var container = document.getElementById('container2');
  var educationSection = container.querySelector('.education-section:nth-child(' + educationCount + ')');
  console.log(educationSection)
  educationSection.remove();

  // Remove corresponding display div
  var displayDiv = document.getElementById('displayCollege' + educationCount);
  if (displayDiv) {
    displayDiv.parentNode.remove(); // Remove the parent element of the display div
  }

  // Renumber the remaining education sections
  var educationHeaders = container.getElementsByClassName('education-header');
  for (var i = 0; i < educationHeaders.length; i++) {
    educationHeaders[i].getElementsByTagName('b')[0].innerText = 'Education ' + (i + 1);
    educationHeaders[i].querySelector('.fa-trash-alt').setAttribute('onclick', 'deleteEducation(' + (i + 1) + ')');
  }

  saveEducation();
}

function saveEducation() {
  var containerHtml = document.getElementById('container2').innerHTML;
  var educationContainerHtml = document.getElementById('educationContainer').innerHTML;
  localStorage.setItem('containerHtml', containerHtml);
  localStorage.setItem('educationContainerHtml', educationContainerHtml);
}

function storeEducationData(experienceCount) {
  var educationData = {
    degree: document.getElementById('degreeInput' + experienceCount).value,
    institution: document.getElementById('institution' + experienceCount).value,
    city: document.getElementById('city' + experienceCount).value,
    from: document.getElementById('from' + experienceCount).value,
    to: document.getElementById('to' + experienceCount).value
  };

  // Store educationData in localStorage
  localStorage.setItem('education' + experienceCount, JSON.stringify(educationData));
}
function loadEducation() {
  var containerHtml = localStorage.getItem('containerHtml');
  var educationContainerHtml = localStorage.getItem('educationContainerHtml');
  if (containerHtml && educationContainerHtml) {
    document.getElementById('container2').innerHTML = containerHtml;
    document.getElementById('educationContainer').innerHTML = educationContainerHtml;
  }
  //localStorage.clear();
}

function updateDisplay(educationCount) {
  console.log(educationCount);
  var institutionInput = document.getElementById('institution' + educationCount);
  var displayCollege = document.getElementById('displayCollege' + educationCount);
  if (institutionInput && displayCollege) {
    displayCollege.innerText = institutionInput.value;
  }

  var degreeInput = document.getElementById('degreeInput' + educationCount);
  var displayDegree = document.getElementById('displayDegree' + educationCount);
  if (degreeInput && displayDegree) {
    displayDegree.innerText = degreeInput.value;
  }

  var cityInput = document.getElementById('city' + educationCount);
  
  var displayCity = document.getElementById('displayCity' + educationCount);
  console.log(displayCity,"jjjjjjjjjjj")
  if (cityInput && displayCity) {
    displayCity.innerText = cityInput.value;
  }

  var fromInput = document.getElementById('degreeFromInput' + educationCount);
  var displayDegreeFrom = document.getElementById('displayDegreeFrom' + educationCount);
  if (fromInput && displayDegreeFrom) {
    displayDegreeFrom.innerText = fromInput.value;
  }

  var toInput = document.getElementById('to' + educationCount);
  var displayDegreeTo = document.getElementById('displayDegreeTo' + educationCount);
  if (toInput && displayDegreeTo) {
    displayDegreeTo.innerText = toInput.value;
  }

  localStorage.setItem("institution" + educationCount, institutionInput.value);
  localStorage.setItem("degreeInput" + educationCount, degreeInput.value);
  localStorage.setItem("city" + educationCount, cityInput.value);
  localStorage.setItem("from" + educationCount, fromInput.value);
  localStorage.setItem("to" + educationCount, toInput.value);
}


function toggleEducation(header) {
  var content = header.nextElementSibling;
  header.querySelector('i').classList.toggle('fa-chevron-down');
  header.querySelector('i').classList.toggle('fa-chevron-up');
  content.classList.toggle('hidden');
}




function projects() {
  var container = document.getElementById('container3');
  container.classList.toggle('hidden');
}

function addNewProject() {
  var container = document.getElementById('container3');
  var projectCount = container.getElementsByClassName('project-section1').length + 1;
  var newProject = document.createElement('div');
  newProject.classList.add('project-section1');

  var header = document.createElement('div');
  header.classList.add('project-header');
  header.onclick = function () { toggleProject(this) };
  header.innerHTML = '<i class="fas fa-chevron-down"></i><p><b>Projects ' + projectCount + '</b></p>'+  '<i class="fas fa-trash-alt" onclick="deleteProjectNew(' + projectCount + ')"></i>'; ;

  var content = document.createElement('div');
  content.classList.add('project-content');
  var formId = 'project1' + projectCount;
  console.log('Form ID:', formId); // Log the form ID

  content.innerHTML = '<form id="project1' + projectCount + '">' +
    '<div class="form-group">' +
    '<input type="text" id="projectName' + projectCount + '" class="form-control" placeholder="Project Name" name="company' + projectCount + '" oninput="updateProjectName2(' + projectCount + ')" style="height: 30px;">' +
    '</div>' +
    '<div class="form-group">' +
    '<label for="description' + projectCount + '">Tools used:</label>' +
    '<textarea id="toolsUsed' + projectCount + '" oninput="updateProjectName2(' + projectCount + ')" class="form-control" name="description' + projectCount + '" rows="3"></textarea>' +
    '</div>' +
    '<div class="form-group">' +
    '<label for="description' + projectCount + '">Link:</label>' +
    '<input type="text" id="link' + projectCount + '" class="form-control" placeholder="Link" name="jobtitle' + projectCount + '" oninput="updateProjectName2(' + projectCount + ')" style="height: 30px;">' +
    '</div>' +
    '<div class="form-group">' +
    '<label for="description' + projectCount + '">Description:</label>' +
    '<textarea id="description' + projectCount + '" oninput="updateProjectName2(' + projectCount + ')" class="form-control" name="description' + projectCount + '" rows="5"></textarea>' +
    '</div>' +
    '</form>';

  newProject.appendChild(header);
  newProject.appendChild(content);
  container.insertBefore(newProject, container.lastElementChild);

  // Create unique IDs for the display div and project section
  var displayDivId = 'displayDiv' + projectCount;
  var projectSectionId = 'project-section' + projectCount;

  var displayDiv = generateProjectDisplayDiv(projectCount, displayDivId, projectSectionId);
  var projectsContainer = document.getElementById('projectsContainer');
  projectsContainer.appendChild(displayDiv);

  saveProject(projectCount);
}

// Function to generate project display div
function generateProjectDisplayDiv(projectCount, displayDivId, projectSectionId) {
  var displayDiv = document.createElement('div');
  displayDiv.classList.add('projects');
  displayDiv.style.marginTop = "10px";
  displayDiv.id = displayDivId;

  displayDiv.innerHTML =
    '<div id="' + projectSectionId + '>' +
   
    ' <p class="job-title" id="pjt' + projectCount + '" style="font-size: 14px; line-height:15px;">' +
    '<span id="displayProjectName' + projectCount + '">'+'<b>Fees Management System</b></span>' +
    '</p>' +
    '<p id="displayProjectTools' + projectCount + '" style="font-size: 14px;line-height:15px;">' +'<strong>'+ 'Tools used :'+ '</strong>'+
   'Python, Django, MySQL, Excel' +
    '</p>' +
    '<p id="displayProjectLink' + projectCount + '"style="font-size: 14px; line-height: 2px;">' +
    'https://www.kickresume.com/dashboard/resumes/' +
    '</p>' +
    


    '<p id="displayProjectDes' + projectCount + '"  style="font-size: 14px; line-height:20px">' +
    'Designing end-to-end experience for financial products on mobile & web platforms. Working closely with managers, marketing specialists, and developers.' +
    '</p>' +

    '</div>';

  return displayDiv;
}

function saveProject() {
  var containerHtml = document.getElementById('container3').innerHTML;
  var projectContainerHtml = document.getElementById('projectsContainer').innerHTML;
  localStorage.setItem('containerHtml', containerHtml);
  localStorage.setItem('projectContainerHtml', projectContainerHtml);
  
}


function loadProject() {
  var containerHtml = localStorage.getItem('containerHtml');
  var projectContainerHtml = localStorage.getItem('projectContainerHtml');
  if (containerHtml && projectContainerHtml) {
    document.getElementById('container3').innerHTML = containerHtml;
    document.getElementById('projectsContainer').innerHTML = projectContainerHtml;
  }
  //localStorage.clear()
}


function updateProjectName2(projectCount) {
  var projectNameInputValue = document.getElementById('projectName' + projectCount).value;
  document.getElementById('displayProjectName' + projectCount).innerText = projectNameInputValue;

  var toolsUsedInputValue = document.getElementById('toolsUsed' + projectCount).value;
  document.getElementById('displayProjectTools' + projectCount).innerText = 'Tools used: ' + toolsUsedInputValue;

  var linkInputValue = document.getElementById('link' + projectCount).value;
  document.getElementById('displayProjectLink' + projectCount).innerText = linkInputValue;

  var descriptionInputValue = document.getElementById('description' + projectCount).value;
  document.getElementById('displayProjectDes' + projectCount).innerText = descriptionInputValue;

  // Store the updated values in localStorage
  localStorage.setItem('projectName' + projectCount, projectNameInputValue);
  localStorage.setItem('toolsUsed' + projectCount, toolsUsedInputValue);
  localStorage.setItem('link' + projectCount, linkInputValue);
  localStorage.setItem('description' + projectCount, descriptionInputValue);
}

function deleteProject(projectCount) {
  var container = document.getElementById('container3');
  var projectSection = container.querySelector('.project-section1:nth-child(' + projectCount + ')');
  projectSection.remove();

  // Remove corresponding display div
  var displayDiv = document.getElementById('displayDiv' + projectCount);
  if (displayDiv) {
    displayDiv.remove();
  }

  // Renumber the remaining project sections
  var projectHeaders = container.getElementsByClassName('project-header');
  for (var i = 0; i < projectHeaders.length; i++) {
    projectHeaders[i].getElementsByTagName('b')[0].innerText = 'Projects ' + (i + 1);
    projectHeaders[i].querySelector('.fa-trash-alt').setAttribute('onclick', 'deleteProject(' + (i + 1) + ')');
  }

  saveProjects();
}

function addNewProject() {
  // Your existing addNewProject function remains unchanged

  // Inside addNewProject function, update the delete icon with the proper onclick event
  header.innerHTML = '<i class="fas fa-chevron-down"></i><p><b>Projects ' + projectCount + '</b></p>' +
    '<i class="fas fa-trash-alt" onclick="deleteProject(' + projectCount + ')"></i>';

  // Your existing code for adding a new project section continues...
}


function loadProjectData(projectCount) {
  // Load project name from localStorage
  var projectNameInput = document.getElementById("projectName" + projectCount);
  if (projectNameInput) {
    var storedValue = localStorage.getItem("dynamicProjectNameLocal" + projectCount);
    if (storedValue) {
      projectNameInput.value = storedValue;
      updateProjectName2(projectCount); // Update the display immediately
    }
  }
}
function toggleProject(header) {
  var content = header.nextElementSibling;
  header.querySelector('i').classList.toggle('fa-chevron-down');
  header.querySelector('i').classList.toggle('fa-chevron-up');
  content.classList.toggle('hidden');
}


function toggleContainer() {
  var container = document.getElementById('profile');
  container.classList.toggle('hidden');
}


function toggleSummary() {
  var container = document.getElementById('summary');
  container.classList.toggle('hidden');
}


function toggleAchievements() {
  var container = document.getElementById('achievements');
  container.classList.toggle('hidden');
}


function toggleSkills() {
  var container = document.getElementById('skills');
  container.classList.toggle('hidden');
}


function toggleLanguages() {
  var container = document.getElementById('languages');
  container.classList.toggle('hidden');
}


function workexperience() {
  var container = document.getElementById('container1');
  container.classList.toggle('hidden');
}
function addNewExperience() {
  var container = document.getElementById('container1');
  var experienceCount = container.getElementsByClassName('experience-section').length + 1;
  var newExperience = document.createElement('div');
  newExperience.classList.add('experience-section');

  var header = document.createElement('div');
  header.classList.add('experience-header');
  header.onclick = function () { toggleExperience(this) };
  header.innerHTML = '<i class="fas fa-chevron-down"></i><p><b>Experience ' + experienceCount + '</b></p>'+
  '<i class="fas fa-trash-alt" onclick="deleteExperience(' + experienceCount + ')"></i>';

  var content = document.createElement('div');
  content.classList.add('experience-content');

  var formId = 'experience' + experienceCount;
  var jobtitleInputId = 'jobtitle' + experienceCount;
  var companyInputId = 'company' + experienceCount;
  var fromInputId = 'from' + experienceCount;
  var toInputId = 'to' + experienceCount;
  var descriptionInputId = 'description' + experienceCount;

  content.innerHTML = '<form id="' + formId + '">' +
    '<div class="form-group">' +
    '<input type="text" id="' + jobtitleInputId + '" class="form-control" placeholder="Designation" name="' + jobtitleInputId + '" style="height: 30px;" oninput="updateExperience2(' + experienceCount + ')">' +
    '</div>' +
    '<div class="form-group">' +
    '<input type="text" id="' + companyInputId + '" class="form-control" placeholder="Company Name" name="' + companyInputId + '" style="height: 30px;" oninput="updateExperience2(' + experienceCount + ')">' +
    '</div>' +
    '<div class="form-group">' +
    '<label for="' + fromInputId + '" style="margin-right: 10px;">From:</label>' +
    '<input type="month" id="' + fromInputId + '" name="' + fromInputId + '" class="form-control" style="height: 35px;" oninput="updateExperience2(' + experienceCount + ')">' +
    '</div>' +
    '<div class="form-group">' +
    '<label for="' + toInputId + '" style="margin-right: 10px;">To:</label>' +
    '<input type="month" id="' + toInputId + '" class="form-control" name="' + toInputId + '" style="height: 35px;" onchange="updateExperience2(' + experienceCount + ')">' +
    '<label for="present' + experienceCount + '" style="margin-left: 10px;">' +
    '<input type="checkbox" id="present' + experienceCount + '" onchange="handlePresentCheckboxExperience(' + experienceCount + ')"> Present' +
    '</label>' +
    '</div>' +
    '<div class="form-group">' +
    '<label for="' + descriptionInputId + '">Description:</label>' +
    '<textarea id="' + descriptionInputId + '" class="form-control" name="' + descriptionInputId + '" rows="5" oninput="updateExperience2(' + experienceCount + ')"></textarea>' +
    '</div>' +
    '</form>';

  newExperience.appendChild(header);
  newExperience.appendChild(content);
  container.insertBefore(newExperience, container.lastElementChild);

  // Generate display div for the new experience section
  var displayDiv = generateExperienceDisplayDiv(experienceCount);
  document.getElementById('experienceContainer').appendChild(displayDiv);
  saveExperience();
}

function generateExperienceDisplayDiv(experienceCount) {
  var displayDiv = document.createElement('div');
  displayDiv.classList.add('work-experience');
  displayDiv.style.marginTop = "10px";

  displayDiv.innerHTML = 
  '<div id="exp' + experienceCount + '">' +     
  '<p class="job-title" id="Display_Designation' + experienceCount + '" style="font-size: 14px;">' +
  'Product Designer' +
  '</p>' +
  '<p style="font-size: 14px;">' +
  '<span id="Display_Cname' + experienceCount + '"> Fintef</span>'+ '</p> '+ '<p style="font-size: 14px; line-height: 1px;">'+'<span id="Display_From' + experienceCount + '"> 2019 </span >-<span id="Display_To' + experienceCount + '"> Present</span>' +
  '</p>' +
  
  '<p id="Display_Description' + experienceCount + '"  style="font-size: 14px;">' +
  'Designing end-to-end experience for financial products on mobile & web platforms. Working closely with managers, marketing specialists, and developers.' +
  '</p>' +
  
  '</div>';

  return displayDiv;
}
function deleteExperience(experienceCount) {
  var container = document.getElementById('container1');
  var experienceSection = container.querySelector('.experience-section:nth-child(' + experienceCount + ')');
  if (experienceSection) {
    experienceSection.remove();
  }

  // Remove corresponding display div
  var displayDiv = document.getElementById('exp' + experienceCount);
  if (displayDiv) {
    displayDiv.parentNode.remove(); // Remove the parent element of the display div
  }

  // Renumber the remaining education sections
  var experienceHeaders = container.getElementsByClassName('experience-header');
  for (var i = 0; i < experienceHeaders.length; i++) {
    experienceHeaders[i].getElementsByTagName('b')[0].innerText = 'Experience ' + (i + 1);
    experienceHeaders[i].querySelector('.fa-trash-alt').onclick = function() {
      deleteExperience(i + 1);
    };
  }

  saveExperience();
}


function saveExperience() {
  var containerHtml = document.getElementById('container1').innerHTML;
  var experienceContainerHtml = document.getElementById('experienceContainer').innerHTML;
  localStorage.setItem('experienceContainerHtml', experienceContainerHtml);
  localStorage.setItem('containerHtml', containerHtml);
}

function loadExperience() {
  var containerHtml = localStorage.getItem('containerHtml');
  var experienceContainerHtml = localStorage.getItem('experienceContainerHtml');
  if (containerHtml && experienceContainerHtml) {
    document.getElementById('container1').innerHTML = containerHtml;
    document.getElementById('experienceContainer').innerHTML = experienceContainerHtml;
  }
 // localStorage.clear();
}
function updateExperience2(experienceCount) {
  console.log(experienceCount);
  var jobtitleValue2 = document.getElementById('jobtitle' + experienceCount).value;
  var jobTitleDisplay = document.getElementById('Display_Designation' + experienceCount);
  if (jobTitleDisplay) {
    jobTitleDisplay.innerText = jobtitleValue2;
  }

  var companyValue2 = document.getElementById('company' + experienceCount).value;
  var companyNameDisplay = document.getElementById('Display_Cname' + experienceCount);
  if (companyNameDisplay) {
    companyNameDisplay.innerText = companyValue2;
  }

  var desValue2 = document.getElementById('description' + experienceCount).value;
  var descriptionDisplay = document.getElementById('Display_Description' + experienceCount);
  if (descriptionDisplay) {
    descriptionDisplay.innerText = desValue2;
  }

  var fromValue2 = document.getElementById('from' + experienceCount).value;
  var fromDisplay = document.getElementById('Display_From' + experienceCount);
  if (fromDisplay) {
    fromDisplay.innerText = fromValue2;
  }

  var toValue2 = document.getElementById('to' + experienceCount).value;
  var toDisplay = document.getElementById('Display_To' + experienceCount);
  if (toDisplay) {
    toDisplay.innerText = toValue2;
  }
}
function handlePresentCheckboxExperience(experienceCount) {
  console.log("gggggggggggggg")
  var toInput = document.getElementById("to" + experienceCount);
  var toContainer = document.getElementById("Display_To" + experienceCount);

  if (document.getElementById("present" + experienceCount).checked) {
    toInput.disabled = true;
    toContainer.innerText = "Present";
  } else {
    toInput.disabled = false;
    updateExperience2(experienceCount);
  }
}
function toggleExperience(header) {
  var content = header.nextElementSibling;
  header.querySelector('i').classList.toggle('fa-chevron-down');
  header.querySelector('i').classList.toggle('fa-chevron-up');
  content.classList.toggle('hidden');
}






var languageCounter1 = 1; // Initial counter for column1 (odd)
    var languageCounter2 = 2; // Initial counter for column3 (even)

    function addLanguageInputFields(columnId1, columnId2) {
      languageCounter1 += 2; // Increment by 2 to get odd numbers
      languageCounter2 += 2; // Increment by 2 to get even numbers

      // Create new input field
      var newInput = document.createElement("input");
      newInput.type = "text";
      newInput.className = "form-control";
      newInput.setAttribute("onkeyup", "updateText()");

      // Create new label
      var newLabel = document.createElement("label");

      // Get the specified containers and insert new label and input field
      var container1 = document.getElementById("languageContainer1");
      newLabel.textContent = "Language (" + languageCounter1 + "):";
      newInput.id = "languageInput" + languageCounter1;
      console.log(newInput.id)
      container1.appendChild(newLabel.cloneNode(true));
      container1.appendChild(newInput.cloneNode(true));

      var container3 = document.getElementById("languageContainer3");
      newLabel.textContent = "Language (" + languageCounter2 + "):";
      newInput.id = "languageInput" + languageCounter2;
      console.log(newInput.id)
      container3.appendChild(newLabel.cloneNode(true));
      container3.appendChild(newInput.cloneNode(true));
    }

    function updateText() {
      // Your updateText function logic here
    }
    function openPopup() {
      // Show the popup
      document.getElementById('imagePopup').style.display = 'block';
    }

    function closePopup() {
      // Close the popup
      document.getElementById('imagePopup').style.display = 'none';
    }

    $(document).ready(function () {
      // Attach input event to all input fields
      $("input").on("input", function () {
        // Get the input value
        var inputValue = $(this).val();

        // Get the corresponding template field id
        var templateField = $(this).data("template-field");

        // Update the template with the input value
        $("#" + templateField).text(inputValue);
      });

      // Add similar event handling for textarea
      $("textarea").on("input", function () {
        var inputValue = $(this).val();
        var templateField = $(this).data("template-field");
        $("#" + templateField).text(inputValue);
      });
    });
    
// dynamic ---------------------------------



 // Update the display with the stored values

 




function updateFName_Lname() {
  // Update first name
  var firstNameValue = document.getElementById("firstName").value;
  document.getElementById("Display_Fname").innerText = firstNameValue;

  // Update last name
  var lastNameValue = document.getElementById("lastName").value;
  document.getElementById("Display_Lname").innerText = lastNameValue;

  // Store values in local storage
  localStorage.setItem("firstName", firstNameValue);
  localStorage.setItem("lastName", lastNameValue);
  
}

function updateLinkedin(){
  // Update LinkedIn URL
  var linkedinValue = document.getElementById("linkedin").value;
  document.getElementById("Display_lnkedin").innerText = linkedinValue;
  localStorage.setItem("linkedin", linkedinValue); 
}

function updateEmail(){
  // Update email
  var emailValue = document.getElementById("email").value;
  document.getElementById("Display_Email").innerText = emailValue;
  localStorage.setItem("email", emailValue);
}

function updatePhoneno(){
  // Update phone number
  var phoneNumberValue = document.getElementById("phoneNumber").value;
  document.getElementById("Display_Phoneno").innerText = phoneNumberValue;
  localStorage.setItem("phoneNumber", phoneNumberValue);
}

function updateSummary(){ 
  var SummaryValue = document.getElementById("summary1").value;
  document.getElementById("Display_Summary").innerText = SummaryValue;
  localStorage.setItem("summary1", SummaryValue);
}

function updateProjectname(){ 
  var projectNameValue = document.getElementById("projectName").value;
  var projectNameElement = document.getElementById("displayProjectName")
  projectNameElement.innerHTML = projectNameValue
  localStorage.setItem("projectNameLocal", projectNameValue);
}

function updateProjectTools(){ 
  var projectToolsValue = document.getElementById("projectTools").value;
  var projectToolsElement = document.getElementById("displayTools")
  projectToolsElement.innerHTML = projectToolsValue
  localStorage.setItem("projectToolsLocal", projectToolsValue);
}

function updateProjectLink(){ 
  var projectLinkValue = document.getElementById("projectLink").value;
  var projectLinkElement = document.getElementById("displayProjectLink")
  projectLinkElement.innerHTML = projectLinkValue
  localStorage.setItem("projectLinkLocal", projectLinkValue);
}

function updateProjectDes(){ 
  var projectDesValue = document.getElementById("projectDes").value;
  var projectDesElement = document.getElementById("displayProjectDes")
   // Replace periods with a round dot and a line break
   var formattedValue = projectDesValue.replace(/\.\s*/g, '<br>&bull; ');
    projectDesElement.innerHTML = formattedValue;
  localStorage.setItem("projectDesLocal", projectDesValue);
}


function updateExperience() {
  var inputValue = document.getElementById("jobtitle1").value;
  var divElement = document.getElementById("Display_Designation");
  divElement.innerText = inputValue;
  
  var companyValue = document.getElementById("company1").value;
  var companyNameElement = document.getElementById("Display_Cname");
  companyNameElement.innerText = companyValue;

  var FromValue = document.getElementById("from1").value;
  var FromElement = document.getElementById("Display_From");
  FromElement.innerText = FromValue;

  var ToValue = document.getElementById("to1").value;
  var ToElement = document.getElementById("Display_To");

  // Check if "Present" checkbox is checked
  var presentCheckbox = document.getElementById("present1");
  if (presentCheckbox.checked) {
    ToElement.innerText = "Present";
  } else {
    if (ToValue) {
      ToElement.innerText = ToValue;
    } else {
      ToElement.innerText = "";
    }
  }

  // Save the current value to localStorage
  localStorage.setItem("toValue", ToValue);

  // Store all values in local storage
  localStorage.setItem("jobTitle", inputValue);
  localStorage.setItem("companyName", companyValue);
  localStorage.setItem("from1", FromValue);
}

function handlePresentCheckbox() {
  console.log("kkkkkkkkkkkkkkk")
  var presentCheckbox = document.getElementById("present1");
  var toDateInput = document.getElementById("to1");

  if (presentCheckbox.checked) {
    toDateInput.disabled = true;
  } else {
    toDateInput.disabled = false;
  }

  // Update displayed date
  updateExperience();
}


function updateExperienceDescription() {
  var descriptionValue = document.getElementById("description1").value;
    var descriptionElement = document.getElementById("Display_Description");
    descriptionElement.innerText = descriptionValue;
    descriptionElement.style.fontSize = "12px"; 
    descriptionElement.style.padding = "0px"; 
  
    localStorage.setItem("description", descriptionValue);
}

function updateDegree() {
  var degreeValue = document.getElementById("degreeInput").value;
  var degreeElement = document.getElementById("displayDegree")
  degreeElement.innerHTML = degreeValue
  localStorage.setItem("degreeInputLocal", degreeValue);
}

function updateDegreeYear() {
  var degreeFromValue = document.getElementById("degreeFromInput").value;
  var degreeFromElement = document.getElementById("displayDegreeFrom")
  degreeFromElement.innerHTML = degreeFromValue

  var degreeToValue = document.getElementById("degreeToInput").value;
  var degreeToElement = document.getElementById("displayDegreeTo")
  degreeToElement.innerHTML = degreeToValue

  localStorage.setItem("degreeFromLocal", degreeFromValue);
  localStorage.setItem("degreeToLocal", degreeToValue);
}

function updateInstitution() {
  var collegeValue = document.getElementById("institution1").value;
  var collegeElement = document.getElementById("displayCollege")
  collegeElement.innerHTML = collegeValue
  localStorage.setItem("collegeInputLocal", collegeValue);
}

function updateCityCountry() {
  var cityValue = document.getElementById("city").value;
  var cityElement = document.getElementById("displayCity")
  cityElement.innerHTML = cityValue
  localStorage.setItem("cityLocal", cityValue); 
}
function updateSkills() {
  var skill1 = document.getElementById('skill1').value;
  var skillsList = document.getElementById('skillsList');
  
  // Split input by commas and trim extra spaces
  var skillsArray = skill1.split(',').map(skill => skill.trim());
  
  // Generate the HTML for the skills list
  var skillsHTML = '<ul >';
  skillsArray.forEach(skill => {
    skillsHTML += '<li style"font-size:16px; text-align : left;">' + skill + '</li>';
  });
  skillsHTML += '</ul>';
  
  // Update the content of the skills list
  skillsList.innerHTML = skillsHTML;

  // Store entered skills in localStorage
  localStorage.setItem('enteredSkills', skill1);
}

function updateAchievements() {
  const textarea = document.getElementById('achievementstext');
  const achievementsSection = document.querySelector('.achievements');
  const achievementList = document.getElementById('achievementList');
  const achievementsText = textarea.value;
  
  // Clear existing list
  achievementList.innerHTML = '';

  // Split achievements text by full stops
  const achievementsGroups = achievementsText.split('.').map(group => group.trim());

  // Populate the list with achievements
  achievementsGroups.forEach(group => {
    if (group) {
      const ul = document.createElement('ul');
      ul.style.marginLeft = '0px';
      ul.style.paddingLeft = '0px';
      ul.style.textAlign = 'left'; // Adjust margin-left as needed

      const groupAchievements = group.split(',').map(item => item.trim());

      groupAchievements.forEach(achievement => {
        if (achievement) {
          const li = document.createElement('li');
          li.textContent = achievement;
          li.style.fontSize = '12px';
          
          li.style.lineHeight = '16px';
          li.style.wordWrap = 'break-word';
          ul.appendChild(li);
        }
      });

      achievementList.appendChild(ul);
    }
  });

  // Show the achievements section if there are achievements
  if (achievementsText.trim() !== '') {
    achievementsSection.classList.remove('hidden');
  } else {
    achievementsSection.classList.add('hidden');
  }
}



function retrieveStoredValue() {
  var storedValue = localStorage.getItem("jobTitle");
  var storedCompanyName = localStorage.getItem("companyName");
  var storedDescription = localStorage.getItem("description");
  var storedDegree = localStorage.getItem("degreeInputLocal")
  var storedFromDegree = localStorage.getItem("degreeFromLocal")
  var storedToDegree = localStorage.getItem("degreeToLocal")
  var storedCollege = localStorage.getItem("collegeInputLocal")
  var storedCity = localStorage.getItem("cityLocal")
  var storedProjectName = localStorage.getItem("projectNameLocal")
  var storedProjectTools = localStorage.getItem("projectToolsLocal")
  var storedProjectLink = localStorage.getItem("projectLinkLocal")
  var storedProjectDes = localStorage.getItem("projectDesLocal")
  var storedSkills = localStorage.getItem("enteredSkills")
 

  if (storedValue) {
    document.getElementById("jobtitle1").value = storedValue;
    document.getElementById("Display_Designation").innerText = storedValue;
  }
  if (storedProjectTools) {
    document.getElementById("projectTools").value = storedProjectTools;
    document.getElementById("displayTools").innerText = storedProjectTools;
  }
  if (storedProjectLink) {
    document.getElementById("projectLink").value = storedProjectLink;
    document.getElementById("displayProjectLink").innerText = storedProjectLink;
  }
  if(storedProjectName){
    document.getElementById("projectName").value = storedProjectName
    document.getElementById("displayProjectName").innerHTML = storedProjectName
  }

  if(storedProjectDes){
    var formattedValue = storedProjectDes.replace(/\.\s*/g, '<br>&bull; ');

    document.getElementById("projectDes").value = storedProjectDes;
    document.getElementById("displayProjectDes").innerHTML = formattedValue;
  }
  
  if (storedCompanyName) {
    document.getElementById("company1").value = storedCompanyName;
    document.getElementById("Display_Cname").innerText = storedCompanyName;
  }

  if (storedDescription) {
    document.getElementById("description1").value = storedDescription;
    document.getElementById("Display_Description").innerText = storedDescription;
  }
  if (storedDegree){
    document.getElementById("degreeInput").value = storedDegree
    document.getElementById("displayDegree").innerHTML = storedDegree
  }
  if (storedFromDegree){
    document.getElementById("degreeFromInput").value = storedFromDegree
    document.getElementById("displayDegreeFrom").innerHTML = storedFromDegree
  }
  if (storedToDegree){
    document.getElementById("degreeToInput").value = storedToDegree
    document.getElementById("displayDegreeTo").innerHTML = storedToDegree
  }
  if (storedCollege){
    document.getElementById("institution1").value = storedCollege
    document.getElementById("displayCollege").innerHTML = storedCollege
  }
  if (storedCity){
    document.getElementById('city').value = storedCity
    document.getElementById('displayCity').innerHTML = storedCity
  }
  if (storedSkills){
    document.getElementById('skill1').value = storedSkills
    document.getElementById('skillsList').innerHTML = storedSkills
  }
 
  var storedFirstname = localStorage.getItem("firstName");
  if (storedFirstname) {
    document.getElementById("firstName").value = storedFirstname;
    document.getElementById("Display_Fname").innerText = storedFirstname;
  }

  var storedLastname = localStorage.getItem("lastName");
  if (storedLastname) {
    document.getElementById("lastName").value = storedLastname;
    document.getElementById("Display_Lname").innerText = storedLastname;
  }

  var storedPhoneNumber = localStorage.getItem("phoneNumber");
  if (storedPhoneNumber) {
    document.getElementById("phoneNumber").value = storedPhoneNumber;
    document.getElementById("Display_Phoneno").innerText = storedPhoneNumber;
  }

  var storedEmail = localStorage.getItem("email");
  if (storedEmail) {
    document.getElementById("email").value = storedEmail;
    document.getElementById("Display_Email").innerText = storedEmail;
  }

  var storedLinkedin = localStorage.getItem("linkedin");
  if (storedLinkedin) {
    document.getElementById("linkedin").value = storedLinkedin;
    document.getElementById("Display_lnkedin").innerText = storedLinkedin;
  }
  var storedSummary = localStorage.getItem("summary1");
  if (storedSummary) {
    document.getElementById("summary1").value = storedSummary;
    document.getElementById("Display_Summary").innerText = storedSummary;
  }
  var storedFrom = localStorage.getItem("from1");
  if (storedFrom) {
    document.getElementById("from1").value = storedFrom;
    document.getElementById("Display_From").innerText = storedFrom;
  }
  var skill1 = localStorage.getItem('enteredSkills');
  if (skill1) {
      document.getElementById('skill1').value = skill1;
      updateSkills(); // Corrected function call
  }
      
  handlePresentCheckbox();
  loadEducation();
  loadExperience();
  loadProject();
      }
  

 
// Call the function to retrieve stored value when the page loads
window.onload = retrieveStoredValue;