/**
 * SOAP API Test Script
 * Run with: node test/test-soap.js
 * Make sure the worker is running: npx wrangler dev
 */

const BASE_URL = process.env.API_URL || 'http://localhost:8787';

async function soapRequest(xml) {
  const response = await fetch(`${BASE_URL}/soap`, {
    method: 'POST',
    headers: {
      'Content-Type': 'text/xml; charset=utf-8',
    },
    body: xml
  });
  return {
    status: response.status,
    body: await response.text()
  };
}

async function testRegisterUser(username, email) {
  console.log(`\n=== Testing RegisterUser: ${username} ===`);
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:user="http://example.com/userservice">
  <soap:Body>
    <user:RegisterUser>
      <user:username>${username}</user:username>
      <user:email>${email}</user:email>
    </user:RegisterUser>
  </soap:Body>
</soap:Envelope>`;

  const result = await soapRequest(xml);
  console.log('Status:', result.status);
  console.log('Response:', result.body);
  return result;
}

async function testGetUsers() {
  console.log('\n=== Testing GetUsers ===');
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:user="http://example.com/userservice">
  <soap:Body>
    <user:GetUsers/>
  </soap:Body>
</soap:Envelope>`;

  const result = await soapRequest(xml);
  console.log('Status:', result.status);
  console.log('Response:', result.body);
  return result;
}

async function testGetUser(id) {
  console.log(`\n=== Testing GetUser: ${id} ===`);
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:user="http://example.com/userservice">
  <soap:Body>
    <user:GetUser>
      <user:id>${id}</user:id>
    </user:GetUser>
  </soap:Body>
</soap:Envelope>`;

  const result = await soapRequest(xml);
  console.log('Status:', result.status);
  console.log('Response:', result.body);
  return result;
}

async function runTests() {
  console.log('SOAP API Test Suite');
  console.log('===================');
  console.log(`Target: ${BASE_URL}`);

  try {
    // Test 1: Get initial user list
    await testGetUsers();

    // Test 2: Register a new user
    await testRegisterUser('alice', 'alice@example.com');

    // Test 3: Register another user
    await testRegisterUser('bob', 'bob@example.com');

    // Test 4: Try to register duplicate user
    await testRegisterUser('alice', 'alice2@example.com');

    // Test 5: Get updated user list
    await testGetUsers();

    // Test 6: Get specific user
    await testGetUser(1);

    // Test 7: Get non-existent user
    await testGetUser(999);

    console.log('\n===================');
    console.log('All tests completed!');
  } catch (error) {
    console.error('Test failed:', error.message);
  }
}

runTests();
