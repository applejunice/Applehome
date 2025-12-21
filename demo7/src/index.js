/**
 * Cloudflare Workers SOAP API Demo
 * Implements user registration and user list functionality
 */

// In-memory user storage (use KV for persistence in production)
let users = [
  { id: 1, username: 'admin', email: 'admin@example.com', createdAt: '2024-01-01T00:00:00Z' }
];
let nextId = 2;

// SOAP Namespaces
const SOAP_NS = 'http://schemas.xmlsoap.org/soap/envelope/';
const USER_NS = 'http://example.com/userservice';

/**
 * Parse XML string to extract SOAP body content
 */
function parseSOAPRequest(xmlString) {
  // Extract SOAP Body content
  const bodyMatch = xmlString.match(/<(?:soap:|SOAP-ENV:|soapenv:)?Body[^>]*>([\s\S]*?)<\/(?:soap:|SOAP-ENV:|soapenv:)?Body>/i);
  if (!bodyMatch) {
    throw new Error('Invalid SOAP request: Body not found');
  }

  const body = bodyMatch[1].trim();

  // Detect operation type
  if (body.includes('RegisterUser') || body.includes('registerUser')) {
    return parseRegisterUserRequest(body);
  } else if (body.includes('GetUsers') || body.includes('getUsers') || body.includes('GetUserList') || body.includes('getUserList')) {
    return { operation: 'GetUsers' };
  } else if (body.includes('GetUser') || body.includes('getUser')) {
    return parseGetUserRequest(body);
  }

  throw new Error('Unknown SOAP operation');
}

/**
 * Parse RegisterUser request
 */
function parseRegisterUserRequest(body) {
  const usernameMatch = body.match(/<(?:\w+:)?username[^>]*>([^<]*)<\/(?:\w+:)?username>/i);
  const emailMatch = body.match(/<(?:\w+:)?email[^>]*>([^<]*)<\/(?:\w+:)?email>/i);

  if (!usernameMatch || !emailMatch) {
    throw new Error('RegisterUser requires username and email');
  }

  return {
    operation: 'RegisterUser',
    data: {
      username: usernameMatch[1].trim(),
      email: emailMatch[1].trim()
    }
  };
}

/**
 * Parse GetUser request
 */
function parseGetUserRequest(body) {
  const idMatch = body.match(/<(?:\w+:)?id[^>]*>([^<]*)<\/(?:\w+:)?id>/i) ||
                  body.match(/<(?:\w+:)?userId[^>]*>([^<]*)<\/(?:\w+:)?userId>/i);

  if (!idMatch) {
    throw new Error('GetUser requires id');
  }

  return {
    operation: 'GetUser',
    data: {
      id: parseInt(idMatch[1].trim(), 10)
    }
  };
}

/**
 * Build SOAP response envelope
 */
function buildSOAPResponse(bodyContent, isError = false) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="${SOAP_NS}" xmlns:user="${USER_NS}">
  <soap:Header/>
  <soap:Body>
    ${bodyContent}
  </soap:Body>
</soap:Envelope>`;
}

/**
 * Build SOAP Fault response
 */
function buildSOAPFault(code, message) {
  return buildSOAPResponse(`
    <soap:Fault>
      <faultcode>${code}</faultcode>
      <faultstring>${escapeXml(message)}</faultstring>
    </soap:Fault>
  `, true);
}

/**
 * Escape XML special characters
 */
function escapeXml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

/**
 * Handle RegisterUser operation
 */
function handleRegisterUser(data) {
  // Check if username already exists
  const existingUser = users.find(u => u.username === data.username);
  if (existingUser) {
    return {
      success: false,
      response: buildSOAPFault('soap:Client', `User '${data.username}' already exists`)
    };
  }

  // Create new user
  const newUser = {
    id: nextId++,
    username: data.username,
    email: data.email,
    createdAt: new Date().toISOString()
  };
  users.push(newUser);

  const responseBody = `
    <user:RegisterUserResponse>
      <user:result>
        <user:success>true</user:success>
        <user:message>User registered successfully</user:message>
        <user:user>
          <user:id>${newUser.id}</user:id>
          <user:username>${escapeXml(newUser.username)}</user:username>
          <user:email>${escapeXml(newUser.email)}</user:email>
          <user:createdAt>${newUser.createdAt}</user:createdAt>
        </user:user>
      </user:result>
    </user:RegisterUserResponse>
  `;

  return {
    success: true,
    response: buildSOAPResponse(responseBody)
  };
}

/**
 * Handle GetUsers operation
 */
function handleGetUsers() {
  const usersXml = users.map(user => `
      <user:user>
        <user:id>${user.id}</user:id>
        <user:username>${escapeXml(user.username)}</user:username>
        <user:email>${escapeXml(user.email)}</user:email>
        <user:createdAt>${user.createdAt}</user:createdAt>
      </user:user>`).join('');

  const responseBody = `
    <user:GetUsersResponse>
      <user:result>
        <user:totalCount>${users.length}</user:totalCount>
        <user:users>${usersXml}
        </user:users>
      </user:result>
    </user:GetUsersResponse>
  `;

  return {
    success: true,
    response: buildSOAPResponse(responseBody)
  };
}

/**
 * Handle GetUser operation
 */
function handleGetUser(data) {
  const user = users.find(u => u.id === data.id);

  if (!user) {
    return {
      success: false,
      response: buildSOAPFault('soap:Client', `User with id ${data.id} not found`)
    };
  }

  const responseBody = `
    <user:GetUserResponse>
      <user:result>
        <user:user>
          <user:id>${user.id}</user:id>
          <user:username>${escapeXml(user.username)}</user:username>
          <user:email>${escapeXml(user.email)}</user:email>
          <user:createdAt>${user.createdAt}</user:createdAt>
        </user:user>
      </user:result>
    </user:GetUserResponse>
  `;

  return {
    success: true,
    response: buildSOAPResponse(responseBody)
  };
}

/**
 * Generate WSDL document
 */
function generateWSDL(baseUrl) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<definitions name="UserService"
  targetNamespace="${USER_NS}"
  xmlns="http://schemas.xmlsoap.org/wsdl/"
  xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
  xmlns:tns="${USER_NS}"
  xmlns:xsd="http://www.w3.org/2001/XMLSchema">

  <types>
    <xsd:schema targetNamespace="${USER_NS}">
      <xsd:complexType name="User">
        <xsd:sequence>
          <xsd:element name="id" type="xsd:int"/>
          <xsd:element name="username" type="xsd:string"/>
          <xsd:element name="email" type="xsd:string"/>
          <xsd:element name="createdAt" type="xsd:dateTime"/>
        </xsd:sequence>
      </xsd:complexType>

      <xsd:element name="RegisterUserRequest">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="username" type="xsd:string"/>
            <xsd:element name="email" type="xsd:string"/>
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>

      <xsd:element name="RegisterUserResponse">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="success" type="xsd:boolean"/>
            <xsd:element name="message" type="xsd:string"/>
            <xsd:element name="user" type="tns:User" minOccurs="0"/>
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>

      <xsd:element name="GetUsersRequest">
        <xsd:complexType/>
      </xsd:element>

      <xsd:element name="GetUsersResponse">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="totalCount" type="xsd:int"/>
            <xsd:element name="users">
              <xsd:complexType>
                <xsd:sequence>
                  <xsd:element name="user" type="tns:User" maxOccurs="unbounded"/>
                </xsd:sequence>
              </xsd:complexType>
            </xsd:element>
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>

      <xsd:element name="GetUserRequest">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="id" type="xsd:int"/>
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>

      <xsd:element name="GetUserResponse">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="user" type="tns:User"/>
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>
    </xsd:schema>
  </types>

  <message name="RegisterUserInput">
    <part name="parameters" element="tns:RegisterUserRequest"/>
  </message>
  <message name="RegisterUserOutput">
    <part name="parameters" element="tns:RegisterUserResponse"/>
  </message>

  <message name="GetUsersInput">
    <part name="parameters" element="tns:GetUsersRequest"/>
  </message>
  <message name="GetUsersOutput">
    <part name="parameters" element="tns:GetUsersResponse"/>
  </message>

  <message name="GetUserInput">
    <part name="parameters" element="tns:GetUserRequest"/>
  </message>
  <message name="GetUserOutput">
    <part name="parameters" element="tns:GetUserResponse"/>
  </message>

  <portType name="UserServicePortType">
    <operation name="RegisterUser">
      <input message="tns:RegisterUserInput"/>
      <output message="tns:RegisterUserOutput"/>
    </operation>
    <operation name="GetUsers">
      <input message="tns:GetUsersInput"/>
      <output message="tns:GetUsersOutput"/>
    </operation>
    <operation name="GetUser">
      <input message="tns:GetUserInput"/>
      <output message="tns:GetUserOutput"/>
    </operation>
  </portType>

  <binding name="UserServiceBinding" type="tns:UserServicePortType">
    <soap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
    <operation name="RegisterUser">
      <soap:operation soapAction="${USER_NS}/RegisterUser"/>
      <input><soap:body use="literal"/></input>
      <output><soap:body use="literal"/></output>
    </operation>
    <operation name="GetUsers">
      <soap:operation soapAction="${USER_NS}/GetUsers"/>
      <input><soap:body use="literal"/></input>
      <output><soap:body use="literal"/></output>
    </operation>
    <operation name="GetUser">
      <soap:operation soapAction="${USER_NS}/GetUser"/>
      <input><soap:body use="literal"/></input>
      <output><soap:body use="literal"/></output>
    </operation>
  </binding>

  <service name="UserService">
    <documentation>SOAP API for User Management</documentation>
    <port name="UserServicePort" binding="tns:UserServiceBinding">
      <soap:address location="${baseUrl}/soap"/>
    </port>
  </service>
</definitions>`;
}

/**
 * Main request handler
 */
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, SOAPAction',
    };

    // Handle preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Serve WSDL
    if (path === '/wsdl' || path === '/soap?wsdl') {
      const baseUrl = `${url.protocol}//${url.host}`;
      return new Response(generateWSDL(baseUrl), {
        headers: {
          'Content-Type': 'application/xml',
          ...corsHeaders
        }
      });
    }

    // API documentation page
    if (path === '/' || path === '/docs') {
      return new Response(getDocsHTML(url.origin), {
        headers: {
          'Content-Type': 'text/html',
          ...corsHeaders
        }
      });
    }

    // Handle SOAP requests
    if (path === '/soap' && request.method === 'POST') {
      try {
        const xmlBody = await request.text();
        const parsed = parseSOAPRequest(xmlBody);

        let result;
        switch (parsed.operation) {
          case 'RegisterUser':
            result = handleRegisterUser(parsed.data);
            break;
          case 'GetUsers':
            result = handleGetUsers();
            break;
          case 'GetUser':
            result = handleGetUser(parsed.data);
            break;
          default:
            result = {
              success: false,
              response: buildSOAPFault('soap:Client', 'Unknown operation')
            };
        }

        return new Response(result.response, {
          status: result.success ? 200 : 400,
          headers: {
            'Content-Type': 'text/xml; charset=utf-8',
            ...corsHeaders
          }
        });
      } catch (error) {
        return new Response(buildSOAPFault('soap:Server', error.message), {
          status: 500,
          headers: {
            'Content-Type': 'text/xml; charset=utf-8',
            ...corsHeaders
          }
        });
      }
    }

    return new Response('Not Found', { status: 404 });
  }
};

/**
 * Generate HTML documentation page
 */
function getDocsHTML(origin) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SOAP API Demo - User Service</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
    h1 { color: #333; }
    h2 { color: #666; border-bottom: 2px solid #ddd; padding-bottom: 10px; }
    .endpoint { background: #fff; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    pre { background: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 5px; overflow-x: auto; font-size: 13px; }
    code { font-family: 'Monaco', 'Menlo', monospace; }
    .method { display: inline-block; padding: 4px 8px; border-radius: 4px; font-weight: bold; margin-right: 10px; }
    .post { background: #49cc90; color: white; }
    .get { background: #61affe; color: white; }
    a { color: #007bff; }
  </style>
</head>
<body>
  <h1>SOAP API Demo - User Service</h1>
  <p>A simple SOAP web service for user management, powered by Cloudflare Workers.</p>

  <h2>Endpoints</h2>

  <div class="endpoint">
    <h3><span class="method get">GET</span>/wsdl</h3>
    <p>Get the WSDL document describing this service.</p>
    <p><a href="${origin}/wsdl" target="_blank">View WSDL</a></p>
  </div>

  <div class="endpoint">
    <h3><span class="method post">POST</span>/soap</h3>
    <p>SOAP endpoint for all operations.</p>
  </div>

  <h2>Operations</h2>

  <div class="endpoint">
    <h3>1. RegisterUser - Register a new user</h3>
    <p><strong>Request:</strong></p>
    <pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:user="http://example.com/userservice"&gt;
  &lt;soap:Body&gt;
    &lt;user:RegisterUser&gt;
      &lt;user:username&gt;john_doe&lt;/user:username&gt;
      &lt;user:email&gt;john@example.com&lt;/user:email&gt;
    &lt;/user:RegisterUser&gt;
  &lt;/soap:Body&gt;
&lt;/soap:Envelope&gt;</code></pre>

    <p><strong>cURL Example:</strong></p>
    <pre><code>curl -X POST ${origin}/soap \\
  -H "Content-Type: text/xml" \\
  -d '&lt;?xml version="1.0"?&gt;&lt;soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:user="http://example.com/userservice"&gt;&lt;soap:Body&gt;&lt;user:RegisterUser&gt;&lt;user:username&gt;john_doe&lt;/user:username&gt;&lt;user:email&gt;john@example.com&lt;/user:email&gt;&lt;/user:RegisterUser&gt;&lt;/soap:Body&gt;&lt;/soap:Envelope&gt;'</code></pre>
  </div>

  <div class="endpoint">
    <h3>2. GetUsers - Get all registered users</h3>
    <p><strong>Request:</strong></p>
    <pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:user="http://example.com/userservice"&gt;
  &lt;soap:Body&gt;
    &lt;user:GetUsers/&gt;
  &lt;/soap:Body&gt;
&lt;/soap:Envelope&gt;</code></pre>

    <p><strong>cURL Example:</strong></p>
    <pre><code>curl -X POST ${origin}/soap \\
  -H "Content-Type: text/xml" \\
  -d '&lt;?xml version="1.0"?&gt;&lt;soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:user="http://example.com/userservice"&gt;&lt;soap:Body&gt;&lt;user:GetUsers/&gt;&lt;/soap:Body&gt;&lt;/soap:Envelope&gt;'</code></pre>
  </div>

  <div class="endpoint">
    <h3>3. GetUser - Get a specific user by ID</h3>
    <p><strong>Request:</strong></p>
    <pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:user="http://example.com/userservice"&gt;
  &lt;soap:Body&gt;
    &lt;user:GetUser&gt;
      &lt;user:id&gt;1&lt;/user:id&gt;
    &lt;/user:GetUser&gt;
  &lt;/soap:Body&gt;
&lt;/soap:Envelope&gt;</code></pre>
  </div>

  <h2>Try It</h2>
  <div class="endpoint">
    <button onclick="testRegister()">Test Register User</button>
    <button onclick="testGetUsers()">Test Get Users</button>
    <pre id="result" style="min-height: 100px;">Click a button to test the API...</pre>
  </div>

  <script>
    async function testRegister() {
      const xml = \`<?xml version="1.0"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:user="http://example.com/userservice"><soap:Body><user:RegisterUser><user:username>test_user_\${Date.now()}</user:username><user:email>test\${Date.now()}@example.com</user:email></user:RegisterUser></soap:Body></soap:Envelope>\`;
      const res = await fetch('/soap', { method: 'POST', headers: { 'Content-Type': 'text/xml' }, body: xml });
      document.getElementById('result').textContent = formatXml(await res.text());
    }

    async function testGetUsers() {
      const xml = '<?xml version="1.0"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:user="http://example.com/userservice"><soap:Body><user:GetUsers/></soap:Body></soap:Envelope>';
      const res = await fetch('/soap', { method: 'POST', headers: { 'Content-Type': 'text/xml' }, body: xml });
      document.getElementById('result').textContent = formatXml(await res.text());
    }

    function formatXml(xml) {
      let formatted = '', indent = '';
      xml.split(/(<[^>]+>)/g).forEach(node => {
        if (node.match(/^<\\/\\w/)) indent = indent.slice(2);
        if (node.match(/^<[^?!\\/]/)) { formatted += indent + node + '\\n'; if (!node.match(/\\/>$/)) indent += '  '; }
        else if (node.match(/^<\\//)) formatted += indent + node + '\\n';
        else if (node.trim()) formatted += indent + node.trim() + '\\n';
      });
      return formatted;
    }
  </script>
</body>
</html>`;
}
