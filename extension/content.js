// Basic data to auto fill. In a real extension, you might collect these
// from user input and store them using chrome.storage.
const profile = {
  firstName: 'John',
  lastName: 'Doe',
  email: 'john.doe@example.com',
  phone: '555-123-4567'
};

function fillFields() {
  const mappings = {
    'input[name="firstName"], input[name*="first_name"]': profile.firstName,
    'input[name="lastName"], input[name*="last_name"]': profile.lastName,
    'input[name="email"]': profile.email,
    'input[type="tel"], input[name="phone"]': profile.phone
  };

  for (const selector in mappings) {
    const el = document.querySelector(selector);
    if (el) {
      el.value = mappings[selector];
      el.dispatchEvent(new Event('input', { bubbles: true }));
    }
  }
}

function autoApply() {
  fillFields();
  // Attempt to submit the form. This may or may not work depending on the page.
  const submitBtn = document.querySelector('button[type="submit"], input[type="submit"]');
  if (submitBtn) {
    submitBtn.click();
  }
}

chrome.runtime.onMessage.addListener((msg) => {
  if (msg.action === 'fill') {
    fillFields();
  } else if (msg.action === 'apply') {
    autoApply();
  }
});
