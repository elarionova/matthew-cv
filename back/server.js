const http = require('http');
const url = require('url');
const fs = require('fs');

function GetHost() {
  if (process.env.OPENSHIFT_NODEJS_IP)
    return process.env.OPENSHIFT_NODEJS_IP;
  return '0.0.0.0';
}

function GetPort() {
  if (process.env.OPENSHIFT_NODEJS_PORT)
    return process.env.OPENSHIFT_NODEJS_PORT;
  return 8000;
}

const hostname = GetHost();
const port = GetPort();
const kIndexPath = '/index.html';

function Respond500(res) {
  res.statusCode = 500;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Something bad happend. Please, try again later\n');
}

function Serve(res, path) {
  res.statusCode = 200;
  const info = static_files[path];
  res.setHeader('Content-Type', info['content-type']);
  res.setHeader('Content-Size', info['size']);
  res.end(info['data']);
}

function OnRequest(req, res) {
  if (req.url == '/')
    return Serve(res, kIndexPath);
  const url_options = url.parse(req.url);
  if (static_files.hasOwnProperty(url_options.pathname))
    return Serve(res, url_options.pathname);
  res.statusCode = 404;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Page not found\n');
}

function GetContentType(path) {
  const mimes = {
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.jpeg': 'image/jpeg',
    '.woff': 'application/font-woff',
    '.ttf': 'application/font-ttf',
    '.eot': 'application/vnd.ms-fontobject',
    '.otf': 'application/font-otf',
    '.svg': 'image/svg+xml',
  };
  var content_type = 'text/plain';  // Fallback option.
  Object.keys(mimes).forEach(function(extension) {
    if (path.indexOf(extension) !== -1) {
      content_type = mimes[extension];
    }
  });
  return content_type;
}

function GetFiles(directory) {
  var files = [];
  const entries = fs.readdirSync(directory);
  entries.forEach(function(entrie) {
    const entrie_path = directory + entrie;
    const stat_info = fs.statSync(entrie_path);
    if (stat_info.isFile()) {
      files.push(entrie_path);
    } else if (stat_info.isDirectory()) {
      const new_files = GetFiles(entrie_path + '/');
      files = files.concat(new_files);
    }  // Omit all other type of files.
  });
  return files;
}

function GetStaticFiles() {
  const kStaticFolderPath = './static/';
  var static_files = {};
  GetFiles(kStaticFolderPath).map(function(file_name) {
    const file_path = file_name.substr(kStaticFolderPath.length - 1);
    static_files[file_path] = {
      'content-type': GetContentType(file_path),
      'size': fs.statSync(file_name).size,
      'data': fs.readFileSync(file_name)
    };
  });
  return static_files;
}

const server = http.createServer(OnRequest);
const static_files = GetStaticFiles();

console.assert(static_files[kIndexPath] !== undefined,
               "Index file always should present");

server.listen(port, hostname, function() {
  console.log('Server is running at %s:%s', GetHost(), GetPort());
});
