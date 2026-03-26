#!/usr/bin/env node
'use strict';
const run = require('node:child_process').spawnSync;
const path = require('node:path');
const os = require('node:os');

let useDocker = false;
const r1 = run('which', ['lychee']);
if (r1.status === 1) {
  // lychee is not installed
  const r2 = run('which', ['docker']);
  if (r2.status === 1) {
    // docker is not installed
    console.error('Please install either "lychee" or "docker"');
    process.exit(1);
  } else {
    useDocker = true;
  }
}

// lychee options
const lycheeOptions = [
  '--offline', // don't check external links
  '--format=json', // export as json
  '--include-fragments', // check anchor links
  './output/**/*.html',
];

// run in docker if needed or locally if installed.
let r4;
if (useDocker) {
  r4 = run('docker', [
    'run',
    '--rm',
    '-w',
    '/input',
    '-v',
    `${process.cwd()}:/input`,
    'lycheeverse/lychee:0.14.3-alpine',
  ].concat(lycheeOptions));
} else {
  r4 = run('lychee', lycheeOptions);
}

if (r4.status === 125) {
  console.error('Could not run with docker, are you sure docker is started?');
  console.error('-> Error: ' + r4.stderr.toString());
  process.exit(1);
}

// see https://github.com/lycheeverse/lychee?tab=readme-ov-file#commandline-parameters
const report = JSON.parse(r4.stdout.toString().trim());
const errors = [];
//console.log(report.fail_map);
for (const file in report.fail_map) {
  for (const issue of report.fail_map[file]) {
    errors.push({
      file: 'file://' + path.resolve(file),
      url: issue.url,
      status: issue.status
    });
  }
}

const issues = errors.filter((e) => !(
  // ignore external relative links to other docs
  e.url.endsWith('output/ogma/latest')
  || e.url.endsWith('output/server-sdk/latest/apidoc')
  || e.url.endsWith('output/admin-manual/latest')
  || e.url.endsWith('output/user-manual/latest')

  // ignore empty anchor links (common way to do a no-op link)
  || e.url.endsWith('.html#')

  // ignore duplicate anchor links issues because
  // the "single page" version is both in ./site/page.html and ./page/index.html
  || e.file.endsWith('/page/index.html')

  // ignore one tough error in the page version of the apidoc-examples
  || (e.file.endsWith('/apidoc-examples/site/page.html') && e.url.endsWith('/site/page.html#apidoc__'))
));

if (issues.length > 0) {
  console.log(JSON.stringify(issues, null, 2));
}
console.error(issues.length + ' broken links/anchors found');
if (issues.length > 0) {
  process.exit(1);
}
