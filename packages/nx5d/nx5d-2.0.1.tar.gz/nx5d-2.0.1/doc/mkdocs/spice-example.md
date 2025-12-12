```python
from nx5d.xrd.kmc3 import LocalRepository
import os, sys

from matplotlib.colors import LogNorm
```


```python
repo = LocalRepository()
proposal = repo.pudell13528
```


```python
proposal.r0047.raw
```




<div><svg style="position: absolute; width: 0; height: 0; overflow: hidden">
<defs>
<symbol id="icon-database" viewBox="0 0 32 32">
<path d="M16 0c-8.837 0-16 2.239-16 5v4c0 2.761 7.163 5 16 5s16-2.239 16-5v-4c0-2.761-7.163-5-16-5z"></path>
<path d="M16 17c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
<path d="M16 26c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
</symbol>
<symbol id="icon-file-text2" viewBox="0 0 32 32">
<path d="M28.681 7.159c-0.694-0.947-1.662-2.053-2.724-3.116s-2.169-2.030-3.116-2.724c-1.612-1.182-2.393-1.319-2.841-1.319h-15.5c-1.378 0-2.5 1.121-2.5 2.5v27c0 1.378 1.122 2.5 2.5 2.5h23c1.378 0 2.5-1.122 2.5-2.5v-19.5c0-0.448-0.137-1.23-1.319-2.841zM24.543 5.457c0.959 0.959 1.712 1.825 2.268 2.543h-4.811v-4.811c0.718 0.556 1.584 1.309 2.543 2.268zM28 29.5c0 0.271-0.229 0.5-0.5 0.5h-23c-0.271 0-0.5-0.229-0.5-0.5v-27c0-0.271 0.229-0.5 0.5-0.5 0 0 15.499-0 15.5 0v7c0 0.552 0.448 1 1 1h7v19.5z"></path>
<path d="M23 26h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
<path d="M23 22h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
<path d="M23 18h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
</symbol>
</defs>
</svg>
<style>/* CSS stylesheet for displaying xarray objects in jupyterlab.
 *
 */

:root {
  --xr-font-color0: var(
    --jp-content-font-color0,
    var(--pst-color-text-base rgba(0, 0, 0, 1))
  );
  --xr-font-color2: var(
    --jp-content-font-color2,
    var(--pst-color-text-base, rgba(0, 0, 0, 0.54))
  );
  --xr-font-color3: var(
    --jp-content-font-color3,
    var(--pst-color-text-base, rgba(0, 0, 0, 0.38))
  );
  --xr-border-color: var(
    --jp-border-color2,
    hsl(from var(--pst-color-on-background, white) h s calc(l - 10))
  );
  --xr-disabled-color: var(
    --jp-layout-color3,
    hsl(from var(--pst-color-on-background, white) h s calc(l - 40))
  );
  --xr-background-color: var(
    --jp-layout-color0,
    var(--pst-color-on-background, white)
  );
  --xr-background-color-row-even: var(
    --jp-layout-color1,
    hsl(from var(--pst-color-on-background, white) h s calc(l - 5))
  );
  --xr-background-color-row-odd: var(
    --jp-layout-color2,
    hsl(from var(--pst-color-on-background, white) h s calc(l - 15))
  );
}

html[theme="dark"],
html[data-theme="dark"],
body[data-theme="dark"],
body.vscode-dark {
  --xr-font-color0: var(
    --jp-content-font-color0,
    var(--pst-color-text-base, rgba(255, 255, 255, 1))
  );
  --xr-font-color2: var(
    --jp-content-font-color2,
    var(--pst-color-text-base, rgba(255, 255, 255, 0.54))
  );
  --xr-font-color3: var(
    --jp-content-font-color3,
    var(--pst-color-text-base, rgba(255, 255, 255, 0.38))
  );
  --xr-border-color: var(
    --jp-border-color2,
    hsl(from var(--pst-color-on-background, #111111) h s calc(l + 10))
  );
  --xr-disabled-color: var(
    --jp-layout-color3,
    hsl(from var(--pst-color-on-background, #111111) h s calc(l + 40))
  );
  --xr-background-color: var(
    --jp-layout-color0,
    var(--pst-color-on-background, #111111)
  );
  --xr-background-color-row-even: var(
    --jp-layout-color1,
    hsl(from var(--pst-color-on-background, #111111) h s calc(l + 5))
  );
  --xr-background-color-row-odd: var(
    --jp-layout-color2,
    hsl(from var(--pst-color-on-background, #111111) h s calc(l + 15))
  );
}

.xr-wrap {
  display: block !important;
  min-width: 300px;
  max-width: 700px;
}

.xr-text-repr-fallback {
  /* fallback to plain text repr when CSS is not injected (untrusted notebook) */
  display: none;
}

.xr-header {
  padding-top: 6px;
  padding-bottom: 6px;
  margin-bottom: 4px;
  border-bottom: solid 1px var(--xr-border-color);
}

.xr-header > div,
.xr-header > ul {
  display: inline;
  margin-top: 0;
  margin-bottom: 0;
}

.xr-obj-type,
.xr-array-name {
  margin-left: 2px;
  margin-right: 10px;
}

.xr-obj-type {
  color: var(--xr-font-color2);
}

.xr-sections {
  padding-left: 0 !important;
  display: grid;
  grid-template-columns: 150px auto auto 1fr 0 20px 0 20px;
}

.xr-section-item {
  display: contents;
}

.xr-section-item input {
  display: inline-block;
  opacity: 0;
  height: 0;
}

.xr-section-item input + label {
  color: var(--xr-disabled-color);
  border: 2px solid transparent !important;
}

.xr-section-item input:enabled + label {
  cursor: pointer;
  color: var(--xr-font-color2);
}

.xr-section-item input:focus + label {
  border: 2px solid var(--xr-font-color0) !important;
}

.xr-section-item input:enabled + label:hover {
  color: var(--xr-font-color0);
}

.xr-section-summary {
  grid-column: 1;
  color: var(--xr-font-color2);
  font-weight: 500;
}

.xr-section-summary > span {
  display: inline-block;
  padding-left: 0.5em;
}

.xr-section-summary-in:disabled + label {
  color: var(--xr-font-color2);
}

.xr-section-summary-in + label:before {
  display: inline-block;
  content: "►";
  font-size: 11px;
  width: 15px;
  text-align: center;
}

.xr-section-summary-in:disabled + label:before {
  color: var(--xr-disabled-color);
}

.xr-section-summary-in:checked + label:before {
  content: "▼";
}

.xr-section-summary-in:checked + label > span {
  display: none;
}

.xr-section-summary,
.xr-section-inline-details {
  padding-top: 4px;
  padding-bottom: 4px;
}

.xr-section-inline-details {
  grid-column: 2 / -1;
}

.xr-section-details {
  display: none;
  grid-column: 1 / -1;
  margin-bottom: 5px;
}

.xr-section-summary-in:checked ~ .xr-section-details {
  display: contents;
}

.xr-array-wrap {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: 20px auto;
}

.xr-array-wrap > label {
  grid-column: 1;
  vertical-align: top;
}

.xr-preview {
  color: var(--xr-font-color3);
}

.xr-array-preview,
.xr-array-data {
  padding: 0 5px !important;
  grid-column: 2;
}

.xr-array-data,
.xr-array-in:checked ~ .xr-array-preview {
  display: none;
}

.xr-array-in:checked ~ .xr-array-data,
.xr-array-preview {
  display: inline-block;
}

.xr-dim-list {
  display: inline-block !important;
  list-style: none;
  padding: 0 !important;
  margin: 0;
}

.xr-dim-list li {
  display: inline-block;
  padding: 0;
  margin: 0;
}

.xr-dim-list:before {
  content: "(";
}

.xr-dim-list:after {
  content: ")";
}

.xr-dim-list li:not(:last-child):after {
  content: ",";
  padding-right: 5px;
}

.xr-has-index {
  font-weight: bold;
}

.xr-var-list,
.xr-var-item {
  display: contents;
}

.xr-var-item > div,
.xr-var-item label,
.xr-var-item > .xr-var-name span {
  background-color: var(--xr-background-color-row-even);
  border-color: var(--xr-background-color-row-odd);
  margin-bottom: 0;
  padding-top: 2px;
}

.xr-var-item > .xr-var-name:hover span {
  padding-right: 5px;
}

.xr-var-list > li:nth-child(odd) > div,
.xr-var-list > li:nth-child(odd) > label,
.xr-var-list > li:nth-child(odd) > .xr-var-name span {
  background-color: var(--xr-background-color-row-odd);
  border-color: var(--xr-background-color-row-even);
}

.xr-var-name {
  grid-column: 1;
}

.xr-var-dims {
  grid-column: 2;
}

.xr-var-dtype {
  grid-column: 3;
  text-align: right;
  color: var(--xr-font-color2);
}

.xr-var-preview {
  grid-column: 4;
}

.xr-index-preview {
  grid-column: 2 / 5;
  color: var(--xr-font-color2);
}

.xr-var-name,
.xr-var-dims,
.xr-var-dtype,
.xr-preview,
.xr-attrs dt {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-right: 10px;
}

.xr-var-name:hover,
.xr-var-dims:hover,
.xr-var-dtype:hover,
.xr-attrs dt:hover {
  overflow: visible;
  width: auto;
  z-index: 1;
}

.xr-var-attrs,
.xr-var-data,
.xr-index-data {
  display: none;
  border-top: 2px dotted var(--xr-background-color);
  padding-bottom: 20px !important;
  padding-top: 10px !important;
}

.xr-var-attrs-in + label,
.xr-var-data-in + label,
.xr-index-data-in + label {
  padding: 0 1px;
}

.xr-var-attrs-in:checked ~ .xr-var-attrs,
.xr-var-data-in:checked ~ .xr-var-data,
.xr-index-data-in:checked ~ .xr-index-data {
  display: block;
}

.xr-var-data > table {
  float: right;
}

.xr-var-data > pre,
.xr-index-data > pre,
.xr-var-data > table > tbody > tr {
  background-color: transparent !important;
}

.xr-var-name span,
.xr-var-data,
.xr-index-name div,
.xr-index-data,
.xr-attrs {
  padding-left: 25px !important;
}

.xr-attrs,
.xr-var-attrs,
.xr-var-data,
.xr-index-data {
  grid-column: 1 / -1;
}

dl.xr-attrs {
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: 125px auto;
}

.xr-attrs dt,
.xr-attrs dd {
  padding: 0;
  margin: 0;
  float: left;
  padding-right: 10px;
  width: auto;
}

.xr-attrs dt {
  font-weight: normal;
  grid-column: 1;
}

.xr-attrs dt:hover span {
  display: inline-block;
  background: var(--xr-background-color);
  padding-right: 10px;
}

.xr-attrs dd {
  grid-column: 2;
  white-space: pre-wrap;
  word-break: break-all;
}

.xr-icon-database,
.xr-icon-file-text2,
.xr-no-icon {
  display: inline-block;
  vertical-align: middle;
  width: 1em;
  height: 1.5em !important;
  stroke-width: 0;
  stroke: currentColor;
  fill: currentColor;
}

.xr-var-attrs-in:checked + label > .xr-icon-file-text2,
.xr-var-data-in:checked + label > .xr-icon-database,
.xr-index-data-in:checked + label > .xr-icon-database {
  color: var(--xr-font-color0);
  filter: drop-shadow(1px 1px 5px var(--xr-font-color2));
  stroke-width: 0.8px;
}
</style><pre class='xr-text-repr-fallback'>&lt;xarray.Dataset&gt; Size: 16MB
Dimensions:  (index: 41, images_1: 195, images_2: 487)
Dimensions without coordinates: index, images_1, images_2
Data variables:
    images   (index, images_1, images_2) int32 16MB -2 0 0 0 0 0 ... 0 0 0 0 -2
    theta    (index) float32 164B 54.66 54.71 54.76 54.81 ... 56.56 56.61 56.66
    chi      float32 4B 0.45
    phi      float32 4B 4.0
    tth      (index) float32 164B 105.5 105.6 105.7 105.8 ... 109.3 109.4 109.5
    temp     (index) float32 164B 0.0 0.0 0.0 0.0 0.0 ... 0.0 0.0 0.0 0.0 0.0
    current  (index) float32 164B 15.24 15.22 15.2 15.18 ... 15.07 15.04 15.03</pre><div class='xr-wrap' style='display:none'><div class='xr-header'><div class='xr-obj-type'>xarray.Dataset</div></div><ul class='xr-sections'><li class='xr-section-item'><input id='section-c5d6b0bc-2cbe-42eb-9317-5f7f0c3ea57e' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-c5d6b0bc-2cbe-42eb-9317-5f7f0c3ea57e' class='xr-section-summary'  title='Expand/collapse section'>Dimensions:</label><div class='xr-section-inline-details'><ul class='xr-dim-list'><li><span>index</span>: 41</li><li><span>images_1</span>: 195</li><li><span>images_2</span>: 487</li></ul></div><div class='xr-section-details'></div></li><li class='xr-section-item'><input id='section-3a56ae3a-ba73-40f1-ae26-74b31a8b5885' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-3a56ae3a-ba73-40f1-ae26-74b31a8b5885' class='xr-section-summary'  title='Expand/collapse section'>Coordinates: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'></ul></div></li><li class='xr-section-item'><input id='section-1669bd7e-9612-4b43-972a-b078a856fdd4' class='xr-section-summary-in' type='checkbox'  checked><label for='section-1669bd7e-9612-4b43-972a-b078a856fdd4' class='xr-section-summary' >Data variables: <span>(7)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>images</span></div><div class='xr-var-dims'>(index, images_1, images_2)</div><div class='xr-var-dtype'>int32</div><div class='xr-var-preview xr-preview'>-2 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 -2</div><input id='attrs-87cb4f8a-40cb-4f20-8596-fbaa20ac7517' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-87cb4f8a-40cb-4f20-8596-fbaa20ac7517' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ad8b32ab-36a6-4f90-a574-d910b41e3ce0' class='xr-var-data-in' type='checkbox'><label for='data-ad8b32ab-36a6-4f90-a574-d910b41e3ce0' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[-2,  0,  0, ...,  0,  0, -2],
        [ 0,  0,  0, ...,  0,  0,  0],
        [ 0,  1,  0, ...,  0,  0,  0],
        ...,
        [ 0,  0,  0, ...,  0,  0,  1],
        [ 0,  1,  0, ...,  0,  0,  0],
        [-2,  0,  0, ...,  0,  0, -2]],

       [[-2,  0,  0, ...,  0,  0, -2],
        [ 0,  0,  0, ...,  0,  0,  0],
        [ 0,  0,  0, ...,  0,  0,  0],
        ...,
        [ 0,  0,  0, ...,  0,  0,  0],
        [ 0,  0,  0, ...,  1,  0,  0],
        [-2,  0,  0, ...,  0,  0, -2]],

       [[-2,  0,  0, ...,  0,  0, -2],
        [ 0,  1,  0, ...,  0,  0,  1],
        [ 0,  0,  0, ...,  0,  0,  0],
        ...,
...
        ...,
        [ 0,  0,  0, ...,  0,  0,  0],
        [ 0,  0,  0, ...,  0,  0,  0],
        [-2,  0,  0, ...,  0,  0, -2]],

       [[-2,  0,  0, ...,  0,  0, -2],
        [ 0,  0,  0, ...,  0,  0,  0],
        [ 0,  0,  0, ...,  0,  0,  0],
        ...,
        [ 0,  0,  0, ...,  0,  0,  0],
        [ 0,  0,  0, ...,  0,  0,  0],
        [-2,  0,  0, ...,  0,  0, -2]],

       [[-2,  0,  0, ...,  0,  0, -2],
        [ 0,  0,  0, ...,  0,  0,  0],
        [ 0,  0,  0, ...,  0,  0,  0],
        ...,
        [ 0,  0,  0, ...,  0,  0,  0],
        [ 0,  0,  0, ...,  0,  0,  0],
        [-2,  0,  1, ...,  0,  0, -2]]], shape=(41, 195, 487), dtype=int32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>theta</span></div><div class='xr-var-dims'>(index)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>54.66 54.71 54.76 ... 56.61 56.66</div><input id='attrs-219a9c2f-9e5b-4c6d-bb3a-a91fb451e387' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-219a9c2f-9e5b-4c6d-bb3a-a91fb451e387' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f552cbfc-9b9f-4aec-a7af-568925b97a32' class='xr-var-data-in' type='checkbox'><label for='data-f552cbfc-9b9f-4aec-a7af-568925b97a32' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([54.659023, 54.709023, 54.75902 , 54.809025, 54.859024, 54.909023,
       54.959023, 55.00902 , 55.059025, 55.109024, 55.159023, 55.209023,
       55.25902 , 55.309025, 55.359024, 55.409023, 55.459023, 55.50902 ,
       55.559025, 55.609024, 55.659023, 55.709023, 55.75902 , 55.809025,
       55.859024, 55.909023, 55.959023, 56.00902 , 56.059025, 56.109024,
       56.159023, 56.209023, 56.25902 , 56.309025, 56.359024, 56.409023,
       56.459023, 56.50902 , 56.559025, 56.609024, 56.659023],
      dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>chi</span></div><div class='xr-var-dims'>()</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>0.45</div><input id='attrs-d952a0cf-acd2-4c8c-951a-731978152ab6' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-d952a0cf-acd2-4c8c-951a-731978152ab6' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-07458a85-f028-4058-b893-2e2244af16ba' class='xr-var-data-in' type='checkbox'><label for='data-07458a85-f028-4058-b893-2e2244af16ba' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array(0.45, dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>phi</span></div><div class='xr-var-dims'>()</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>4.0</div><input id='attrs-a6a6ace3-1968-45b4-9499-cf3cf052d08b' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a6a6ace3-1968-45b4-9499-cf3cf052d08b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a7be2ece-ebdb-4502-9d22-aeaf00d67040' class='xr-var-data-in' type='checkbox'><label for='data-a7be2ece-ebdb-4502-9d22-aeaf00d67040' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array(4., dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>tth</span></div><div class='xr-var-dims'>(index)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>105.5 105.6 105.7 ... 109.4 109.5</div><input id='attrs-6a6ff12e-4282-47cd-acef-df7c5d6335e8' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-6a6ff12e-4282-47cd-acef-df7c5d6335e8' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-a96551c6-a335-48b0-a6dc-188e19d5d1e0' class='xr-var-data-in' type='checkbox'><label for='data-a96551c6-a335-48b0-a6dc-188e19d5d1e0' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([105.5, 105.6, 105.7, 105.8, 105.9, 106. , 106.1, 106.2, 106.3,
       106.4, 106.5, 106.6, 106.7, 106.8, 106.9, 107. , 107.1, 107.2,
       107.3, 107.4, 107.5, 107.6, 107.7, 107.8, 107.9, 108. , 108.1,
       108.2, 108.3, 108.4, 108.5, 108.6, 108.7, 108.8, 108.9, 109. ,
       109.1, 109.2, 109.3, 109.4, 109.5], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>temp</span></div><div class='xr-var-dims'>(index)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>0.0 0.0 0.0 0.0 ... 0.0 0.0 0.0 0.0</div><input id='attrs-77a040ec-6d2c-41a0-88ec-57e04907ff09' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-77a040ec-6d2c-41a0-88ec-57e04907ff09' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8376b925-b4bf-4740-8960-cc22bcc323fc' class='xr-var-data-in' type='checkbox'><label for='data-8376b925-b4bf-4740-8960-cc22bcc323fc' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
       0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
       0., 0., 0., 0., 0., 0., 0.], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>current</span></div><div class='xr-var-dims'>(index)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>15.24 15.22 15.2 ... 15.04 15.03</div><input id='attrs-320b7f10-ba13-492c-82e0-68645a8a6a5f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-320b7f10-ba13-492c-82e0-68645a8a6a5f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-0b968211-4bbe-4cde-9635-bdb7b7b8f344' class='xr-var-data-in' type='checkbox'><label for='data-0b968211-4bbe-4cde-9635-bdb7b7b8f344' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([15.241023, 15.222171, 15.20208 , 15.180189, 15.16276 , 15.14391 ,
       15.12225 , 15.101334, 15.081652, 15.061305, 15.04284 , 15.019563,
       15.002664, 14.982075, 14.962416, 15.231249, 15.211234, 15.190819,
       15.154391, 15.147645, 15.126808, 15.110424, 15.076896, 15.067294,
       15.048417, 15.031865, 15.01314 , 14.990672, 14.970047, 15.22843 ,
       15.224754, 15.205817, 15.184592, 15.162649, 15.146963, 15.127585,
       15.103316, 15.085775, 15.068184, 15.041037, 15.025406],
      dtype=float32)</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-545ea650-2558-486e-86c7-e64b5fd577ca' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-545ea650-2558-486e-86c7-e64b5fd577ca' class='xr-section-summary'  title='Expand/collapse section'>Indexes: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'></ul></div></li><li class='xr-section-item'><input id='section-2f6822ab-33e4-4c8f-a4b0-733dafcb67e9' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-2f6822ab-33e4-4c8f-a4b0-733dafcb67e9' class='xr-section-summary'  title='Expand/collapse section'>Attributes: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'></dl></div></li></ul></div></div>




```python
proposal.r0047.spice
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>handle</th>
      <th>clean</th>
      <th>revision</th>
      <th>uuid</th>
      <th>data</th>
    </tr>
    <tr>
      <th>anchor</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>r0047</th>
      <td>exp_info</td>
      <td>True</td>
      <td>11</td>
      <td>2b7298</td>
      <td>{'goniometerAxes': {'theta': 'x+', 'chi': 'y+'...</td>
    </tr>
    <tr>
      <th></th>
      <td>offsets</td>
      <td>True</td>
      <td>1</td>
      <td>533bbe</td>
      <td>{'chi': 0.0, 'phi': 0.0, 'theta': 0.0, 'tth': ...</td>
    </tr>
  </tbody>
</table>
</div>




```python
proposal.r0047.cooked
```




<div><svg style="position: absolute; width: 0; height: 0; overflow: hidden">
<defs>
<symbol id="icon-database" viewBox="0 0 32 32">
<path d="M16 0c-8.837 0-16 2.239-16 5v4c0 2.761 7.163 5 16 5s16-2.239 16-5v-4c0-2.761-7.163-5-16-5z"></path>
<path d="M16 17c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
<path d="M16 26c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
</symbol>
<symbol id="icon-file-text2" viewBox="0 0 32 32">
<path d="M28.681 7.159c-0.694-0.947-1.662-2.053-2.724-3.116s-2.169-2.030-3.116-2.724c-1.612-1.182-2.393-1.319-2.841-1.319h-15.5c-1.378 0-2.5 1.121-2.5 2.5v27c0 1.378 1.122 2.5 2.5 2.5h23c1.378 0 2.5-1.122 2.5-2.5v-19.5c0-0.448-0.137-1.23-1.319-2.841zM24.543 5.457c0.959 0.959 1.712 1.825 2.268 2.543h-4.811v-4.811c0.718 0.556 1.584 1.309 2.543 2.268zM28 29.5c0 0.271-0.229 0.5-0.5 0.5h-23c-0.271 0-0.5-0.229-0.5-0.5v-27c0-0.271 0.229-0.5 0.5-0.5 0 0 15.499-0 15.5 0v7c0 0.552 0.448 1 1 1h7v19.5z"></path>
<path d="M23 26h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
<path d="M23 22h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
<path d="M23 18h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
</symbol>
</defs>
</svg>
<style>/* CSS stylesheet for displaying xarray objects in jupyterlab.
 *
 */

:root {
  --xr-font-color0: var(
    --jp-content-font-color0,
    var(--pst-color-text-base rgba(0, 0, 0, 1))
  );
  --xr-font-color2: var(
    --jp-content-font-color2,
    var(--pst-color-text-base, rgba(0, 0, 0, 0.54))
  );
  --xr-font-color3: var(
    --jp-content-font-color3,
    var(--pst-color-text-base, rgba(0, 0, 0, 0.38))
  );
  --xr-border-color: var(
    --jp-border-color2,
    hsl(from var(--pst-color-on-background, white) h s calc(l - 10))
  );
  --xr-disabled-color: var(
    --jp-layout-color3,
    hsl(from var(--pst-color-on-background, white) h s calc(l - 40))
  );
  --xr-background-color: var(
    --jp-layout-color0,
    var(--pst-color-on-background, white)
  );
  --xr-background-color-row-even: var(
    --jp-layout-color1,
    hsl(from var(--pst-color-on-background, white) h s calc(l - 5))
  );
  --xr-background-color-row-odd: var(
    --jp-layout-color2,
    hsl(from var(--pst-color-on-background, white) h s calc(l - 15))
  );
}

html[theme="dark"],
html[data-theme="dark"],
body[data-theme="dark"],
body.vscode-dark {
  --xr-font-color0: var(
    --jp-content-font-color0,
    var(--pst-color-text-base, rgba(255, 255, 255, 1))
  );
  --xr-font-color2: var(
    --jp-content-font-color2,
    var(--pst-color-text-base, rgba(255, 255, 255, 0.54))
  );
  --xr-font-color3: var(
    --jp-content-font-color3,
    var(--pst-color-text-base, rgba(255, 255, 255, 0.38))
  );
  --xr-border-color: var(
    --jp-border-color2,
    hsl(from var(--pst-color-on-background, #111111) h s calc(l + 10))
  );
  --xr-disabled-color: var(
    --jp-layout-color3,
    hsl(from var(--pst-color-on-background, #111111) h s calc(l + 40))
  );
  --xr-background-color: var(
    --jp-layout-color0,
    var(--pst-color-on-background, #111111)
  );
  --xr-background-color-row-even: var(
    --jp-layout-color1,
    hsl(from var(--pst-color-on-background, #111111) h s calc(l + 5))
  );
  --xr-background-color-row-odd: var(
    --jp-layout-color2,
    hsl(from var(--pst-color-on-background, #111111) h s calc(l + 15))
  );
}

.xr-wrap {
  display: block !important;
  min-width: 300px;
  max-width: 700px;
}

.xr-text-repr-fallback {
  /* fallback to plain text repr when CSS is not injected (untrusted notebook) */
  display: none;
}

.xr-header {
  padding-top: 6px;
  padding-bottom: 6px;
  margin-bottom: 4px;
  border-bottom: solid 1px var(--xr-border-color);
}

.xr-header > div,
.xr-header > ul {
  display: inline;
  margin-top: 0;
  margin-bottom: 0;
}

.xr-obj-type,
.xr-array-name {
  margin-left: 2px;
  margin-right: 10px;
}

.xr-obj-type {
  color: var(--xr-font-color2);
}

.xr-sections {
  padding-left: 0 !important;
  display: grid;
  grid-template-columns: 150px auto auto 1fr 0 20px 0 20px;
}

.xr-section-item {
  display: contents;
}

.xr-section-item input {
  display: inline-block;
  opacity: 0;
  height: 0;
}

.xr-section-item input + label {
  color: var(--xr-disabled-color);
  border: 2px solid transparent !important;
}

.xr-section-item input:enabled + label {
  cursor: pointer;
  color: var(--xr-font-color2);
}

.xr-section-item input:focus + label {
  border: 2px solid var(--xr-font-color0) !important;
}

.xr-section-item input:enabled + label:hover {
  color: var(--xr-font-color0);
}

.xr-section-summary {
  grid-column: 1;
  color: var(--xr-font-color2);
  font-weight: 500;
}

.xr-section-summary > span {
  display: inline-block;
  padding-left: 0.5em;
}

.xr-section-summary-in:disabled + label {
  color: var(--xr-font-color2);
}

.xr-section-summary-in + label:before {
  display: inline-block;
  content: "►";
  font-size: 11px;
  width: 15px;
  text-align: center;
}

.xr-section-summary-in:disabled + label:before {
  color: var(--xr-disabled-color);
}

.xr-section-summary-in:checked + label:before {
  content: "▼";
}

.xr-section-summary-in:checked + label > span {
  display: none;
}

.xr-section-summary,
.xr-section-inline-details {
  padding-top: 4px;
  padding-bottom: 4px;
}

.xr-section-inline-details {
  grid-column: 2 / -1;
}

.xr-section-details {
  display: none;
  grid-column: 1 / -1;
  margin-bottom: 5px;
}

.xr-section-summary-in:checked ~ .xr-section-details {
  display: contents;
}

.xr-array-wrap {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: 20px auto;
}

.xr-array-wrap > label {
  grid-column: 1;
  vertical-align: top;
}

.xr-preview {
  color: var(--xr-font-color3);
}

.xr-array-preview,
.xr-array-data {
  padding: 0 5px !important;
  grid-column: 2;
}

.xr-array-data,
.xr-array-in:checked ~ .xr-array-preview {
  display: none;
}

.xr-array-in:checked ~ .xr-array-data,
.xr-array-preview {
  display: inline-block;
}

.xr-dim-list {
  display: inline-block !important;
  list-style: none;
  padding: 0 !important;
  margin: 0;
}

.xr-dim-list li {
  display: inline-block;
  padding: 0;
  margin: 0;
}

.xr-dim-list:before {
  content: "(";
}

.xr-dim-list:after {
  content: ")";
}

.xr-dim-list li:not(:last-child):after {
  content: ",";
  padding-right: 5px;
}

.xr-has-index {
  font-weight: bold;
}

.xr-var-list,
.xr-var-item {
  display: contents;
}

.xr-var-item > div,
.xr-var-item label,
.xr-var-item > .xr-var-name span {
  background-color: var(--xr-background-color-row-even);
  border-color: var(--xr-background-color-row-odd);
  margin-bottom: 0;
  padding-top: 2px;
}

.xr-var-item > .xr-var-name:hover span {
  padding-right: 5px;
}

.xr-var-list > li:nth-child(odd) > div,
.xr-var-list > li:nth-child(odd) > label,
.xr-var-list > li:nth-child(odd) > .xr-var-name span {
  background-color: var(--xr-background-color-row-odd);
  border-color: var(--xr-background-color-row-even);
}

.xr-var-name {
  grid-column: 1;
}

.xr-var-dims {
  grid-column: 2;
}

.xr-var-dtype {
  grid-column: 3;
  text-align: right;
  color: var(--xr-font-color2);
}

.xr-var-preview {
  grid-column: 4;
}

.xr-index-preview {
  grid-column: 2 / 5;
  color: var(--xr-font-color2);
}

.xr-var-name,
.xr-var-dims,
.xr-var-dtype,
.xr-preview,
.xr-attrs dt {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-right: 10px;
}

.xr-var-name:hover,
.xr-var-dims:hover,
.xr-var-dtype:hover,
.xr-attrs dt:hover {
  overflow: visible;
  width: auto;
  z-index: 1;
}

.xr-var-attrs,
.xr-var-data,
.xr-index-data {
  display: none;
  border-top: 2px dotted var(--xr-background-color);
  padding-bottom: 20px !important;
  padding-top: 10px !important;
}

.xr-var-attrs-in + label,
.xr-var-data-in + label,
.xr-index-data-in + label {
  padding: 0 1px;
}

.xr-var-attrs-in:checked ~ .xr-var-attrs,
.xr-var-data-in:checked ~ .xr-var-data,
.xr-index-data-in:checked ~ .xr-index-data {
  display: block;
}

.xr-var-data > table {
  float: right;
}

.xr-var-data > pre,
.xr-index-data > pre,
.xr-var-data > table > tbody > tr {
  background-color: transparent !important;
}

.xr-var-name span,
.xr-var-data,
.xr-index-name div,
.xr-index-data,
.xr-attrs {
  padding-left: 25px !important;
}

.xr-attrs,
.xr-var-attrs,
.xr-var-data,
.xr-index-data {
  grid-column: 1 / -1;
}

dl.xr-attrs {
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: 125px auto;
}

.xr-attrs dt,
.xr-attrs dd {
  padding: 0;
  margin: 0;
  float: left;
  padding-right: 10px;
  width: auto;
}

.xr-attrs dt {
  font-weight: normal;
  grid-column: 1;
}

.xr-attrs dt:hover span {
  display: inline-block;
  background: var(--xr-background-color);
  padding-right: 10px;
}

.xr-attrs dd {
  grid-column: 2;
  white-space: pre-wrap;
  word-break: break-all;
}

.xr-icon-database,
.xr-icon-file-text2,
.xr-no-icon {
  display: inline-block;
  vertical-align: middle;
  width: 1em;
  height: 1.5em !important;
  stroke-width: 0;
  stroke: currentColor;
  fill: currentColor;
}

.xr-var-attrs-in:checked + label > .xr-icon-file-text2,
.xr-var-data-in:checked + label > .xr-icon-database,
.xr-index-data-in:checked + label > .xr-icon-database {
  color: var(--xr-font-color0);
  filter: drop-shadow(1px 1px 5px var(--xr-font-color2));
  stroke-width: 0.8px;
}
</style><pre class='xr-text-repr-fallback'>&lt;xarray.Dataset&gt; Size: 31MB
Dimensions:  (qy: 41, qx: 195, qz: 487)
Coordinates:
  * qy       (qy) float64 328B -0.2712 -0.2462 -0.2213 ... 0.6774 0.7023 0.7273
  * qx       (qx) float64 2kB -0.3518 -0.349 -0.3462 ... 0.1917 0.1945 0.1973
  * qz       (qz) float64 4kB 10.69 10.69 10.7 10.7 ... 11.68 11.69 11.69 11.69
Data variables:
    images   (qy, qx, qz) float64 31MB 0.0 0.0 0.0 0.0 0.0 ... 0.0 0.0 0.0 0.0
    temp     float64 8B 0.0
    current  float64 8B 15.11</pre><div class='xr-wrap' style='display:none'><div class='xr-header'><div class='xr-obj-type'>xarray.Dataset</div></div><ul class='xr-sections'><li class='xr-section-item'><input id='section-106ead7f-84c4-4606-92d2-cc2b6a69b244' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-106ead7f-84c4-4606-92d2-cc2b6a69b244' class='xr-section-summary'  title='Expand/collapse section'>Dimensions:</label><div class='xr-section-inline-details'><ul class='xr-dim-list'><li><span class='xr-has-index'>qy</span>: 41</li><li><span class='xr-has-index'>qx</span>: 195</li><li><span class='xr-has-index'>qz</span>: 487</li></ul></div><div class='xr-section-details'></div></li><li class='xr-section-item'><input id='section-1d68635b-23e5-4daa-97ca-f70382d23b73' class='xr-section-summary-in' type='checkbox'  checked><label for='section-1d68635b-23e5-4daa-97ca-f70382d23b73' class='xr-section-summary' >Coordinates: <span>(3)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>qy</span></div><div class='xr-var-dims'>(qy)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>-0.2712 -0.2462 ... 0.7023 0.7273</div><input id='attrs-9e5f0ee6-10c3-464e-bda0-4da84d709d9f' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-9e5f0ee6-10c3-464e-bda0-4da84d709d9f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-73c79cf4-7393-4d1e-8489-b74161c9a9fa' class='xr-var-data-in' type='checkbox'><label for='data-73c79cf4-7393-4d1e-8489-b74161c9a9fa' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([-0.271188, -0.246227, -0.221265, -0.196304, -0.171342, -0.14638 ,
       -0.121419, -0.096457, -0.071496, -0.046534, -0.021572,  0.003389,
        0.028351,  0.053312,  0.078274,  0.103235,  0.128197,  0.153159,
        0.17812 ,  0.203082,  0.228043,  0.253005,  0.277967,  0.302928,
        0.32789 ,  0.352851,  0.377813,  0.402774,  0.427736,  0.452698,
        0.477659,  0.502621,  0.527582,  0.552544,  0.577506,  0.602467,
        0.627429,  0.65239 ,  0.677352,  0.702313,  0.727275])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>qx</span></div><div class='xr-var-dims'>(qx)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>-0.3518 -0.349 ... 0.1945 0.1973</div><input id='attrs-d6f0c735-7dfa-4075-a32c-4dcbd50305a2' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-d6f0c735-7dfa-4075-a32c-4dcbd50305a2' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-0b48010c-ac89-41f8-970e-9988f006a4db' class='xr-var-data-in' type='checkbox'><label for='data-0b48010c-ac89-41f8-970e-9988f006a4db' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([-0.351836, -0.349005, -0.346174, -0.343343, -0.340512, -0.337681,
       -0.33485 , -0.33202 , -0.329189, -0.326358, -0.323527, -0.320696,
       -0.317865, -0.315035, -0.312204, -0.309373, -0.306542, -0.303711,
       -0.30088 , -0.298049, -0.295219, -0.292388, -0.289557, -0.286726,
       -0.283895, -0.281064, -0.278233, -0.275403, -0.272572, -0.269741,
       -0.26691 , -0.264079, -0.261248, -0.258417, -0.255587, -0.252756,
       -0.249925, -0.247094, -0.244263, -0.241432, -0.238602, -0.235771,
       -0.23294 , -0.230109, -0.227278, -0.224447, -0.221616, -0.218786,
       -0.215955, -0.213124, -0.210293, -0.207462, -0.204631, -0.2018  ,
       -0.19897 , -0.196139, -0.193308, -0.190477, -0.187646, -0.184815,
       -0.181985, -0.179154, -0.176323, -0.173492, -0.170661, -0.16783 ,
       -0.164999, -0.162169, -0.159338, -0.156507, -0.153676, -0.150845,
       -0.148014, -0.145183, -0.142353, -0.139522, -0.136691, -0.13386 ,
       -0.131029, -0.128198, -0.125367, -0.122537, -0.119706, -0.116875,
       -0.114044, -0.111213, -0.108382, -0.105552, -0.102721, -0.09989 ,
       -0.097059, -0.094228, -0.091397, -0.088566, -0.085736, -0.082905,
       -0.080074, -0.077243, -0.074412, -0.071581, -0.06875 , -0.06592 ,
       -0.063089, -0.060258, -0.057427, -0.054596, -0.051765, -0.048934,
       -0.046104, -0.043273, -0.040442, -0.037611, -0.03478 , -0.031949,
       -0.029119, -0.026288, -0.023457, -0.020626, -0.017795, -0.014964,
       -0.012133, -0.009303, -0.006472, -0.003641, -0.00081 ,  0.002021,
        0.004852,  0.007683,  0.010513,  0.013344,  0.016175,  0.019006,
        0.021837,  0.024668,  0.027498,  0.030329,  0.03316 ,  0.035991,
        0.038822,  0.041653,  0.044484,  0.047314,  0.050145,  0.052976,
        0.055807,  0.058638,  0.061469,  0.0643  ,  0.06713 ,  0.069961,
        0.072792,  0.075623,  0.078454,  0.081285,  0.084116,  0.086946,
        0.089777,  0.092608,  0.095439,  0.09827 ,  0.101101,  0.103931,
        0.106762,  0.109593,  0.112424,  0.115255,  0.118086,  0.120917,
        0.123747,  0.126578,  0.129409,  0.13224 ,  0.135071,  0.137902,
        0.140733,  0.143563,  0.146394,  0.149225,  0.152056,  0.154887,
        0.157718,  0.160548,  0.163379,  0.16621 ,  0.169041,  0.171872,
        0.174703,  0.177534,  0.180364,  0.183195,  0.186026,  0.188857,
        0.191688,  0.194519,  0.19735 ])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>qz</span></div><div class='xr-var-dims'>(qz)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>10.69 10.69 10.7 ... 11.69 11.69</div><input id='attrs-68fbdd4d-a7bb-4182-8049-a10a2fc592b1' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-68fbdd4d-a7bb-4182-8049-a10a2fc592b1' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-24c5746e-3669-4ac3-92e7-077c707e5bb5' class='xr-var-data-in' type='checkbox'><label for='data-24c5746e-3669-4ac3-92e7-077c707e5bb5' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([10.691191, 10.693247, 10.695302, ..., 11.68605 , 11.688106, 11.690161],
      shape=(487,))</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-8c98b3de-b512-4bc4-bc16-a0a76a9cac00' class='xr-section-summary-in' type='checkbox'  checked><label for='section-8c98b3de-b512-4bc4-bc16-a0a76a9cac00' class='xr-section-summary' >Data variables: <span>(3)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>images</span></div><div class='xr-var-dims'>(qy, qx, qz)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0 0.0 0.0 0.0 ... 0.0 0.0 0.0 0.0</div><input id='attrs-b58106b8-2a43-468c-891f-352dd4a0ed1c' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b58106b8-2a43-468c-891f-352dd4a0ed1c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-f58409f5-9499-4deb-ab44-83864d3bb278' class='xr-var-data-in' type='checkbox'><label for='data-f58409f5-9499-4deb-ab44-83864d3bb278' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([[[ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        ...,
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.]],

       [[ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        ...,
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.]],

       [[ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        ...,
...
        ...,
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0., -2., ...,  0.,  0.,  0.]],

       [[ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        ...,
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.]],

       [[ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        ...,
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.],
        [ 0.,  0.,  0., ...,  0.,  0.,  0.]]], shape=(41, 195, 487))</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>temp</span></div><div class='xr-var-dims'>()</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>0.0</div><input id='attrs-0d72334d-0c34-41f4-80ab-d6d2a9a543ee' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-0d72334d-0c34-41f4-80ab-d6d2a9a543ee' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ae12e769-c815-486e-b99e-7b6db12fe135' class='xr-var-data-in' type='checkbox'><label for='data-ae12e769-c815-486e-b99e-7b6db12fe135' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array(0.)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>current</span></div><div class='xr-var-dims'>()</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>15.11</div><input id='attrs-a4fa4035-7561-40cc-8288-f523e2b71e21' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-a4fa4035-7561-40cc-8288-f523e2b71e21' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-d748d76c-3155-49ae-ac33-a9f3c91ab8a4' class='xr-var-data-in' type='checkbox'><label for='data-d748d76c-3155-49ae-ac33-a9f3c91ab8a4' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array(15.10984421)</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-0992360f-7a1f-4610-b14c-44ac73e8ec08' class='xr-section-summary-in' type='checkbox'  ><label for='section-0992360f-7a1f-4610-b14c-44ac73e8ec08' class='xr-section-summary' >Indexes: <span>(3)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-index-name'><div>qy</div></div><div class='xr-index-preview'>PandasIndex</div><input type='checkbox' disabled/><label></label><input id='index-61ede3f4-410d-4416-a2b7-2ea1d92be2f6' class='xr-index-data-in' type='checkbox'/><label for='index-61ede3f4-410d-4416-a2b7-2ea1d92be2f6' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Index([  -0.2711882678144093,    -0.246226684319741,  -0.22126510082507272,
        -0.19630351733040446,  -0.17134193383573618,   -0.1463803503410679,
        -0.12141876684639963,  -0.09645718335173134,  -0.07149559985706305,
       -0.046534016362394764, -0.021572432867726477, 0.0033891506269417837,
        0.028350734121610044,   0.05331231761627836,   0.07827390111094662,
         0.10323548460561494,    0.1281970681002832,   0.15315865159495146,
         0.17812023508961977,   0.20308181858428803,   0.22804340207895635,
          0.2530049855736246,   0.27796656906829287,   0.30292815256296113,
          0.3278897360576294,   0.35285131955229776,     0.377812903046966,
          0.4027744865416343,   0.42773607003630254,    0.4526976535309708,
         0.47765923702563917,    0.5026208205203074,    0.5275824040149757,
           0.552543987509644,    0.5775055710043122,    0.6024671544989806,
          0.6274287379936488,    0.6523903214883171,    0.6773519049829854,
          0.7023134884776536,     0.727275071972322],
      dtype=&#x27;float64&#x27;, name=&#x27;qy&#x27;))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>qx</div></div><div class='xr-index-preview'>PandasIndex</div><input type='checkbox' disabled/><label></label><input id='index-966327d1-0dc2-4943-a25a-f47b0645cce6' class='xr-index-data-in' type='checkbox'/><label for='index-966327d1-0dc2-4943-a25a-f47b0645cce6' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Index([ -0.3518355763756962, -0.34900472517620484,  -0.3461738739767135,
        -0.3433430227772221,  -0.3405121715777308, -0.33768132037823945,
        -0.3348504691787481,  -0.3320196179792567,  -0.3291887667797654,
       -0.32635791558027405,
       ...
         0.1718718955302032,  0.17470274672969455,  0.17753359792918588,
        0.18036444912867722,  0.18319530032816855,     0.18602615152766,
        0.18885700272715134,  0.19168785392664267,    0.194518705126134,
        0.19734955632562534],
      dtype=&#x27;float64&#x27;, name=&#x27;qx&#x27;, length=195))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>qz</div></div><div class='xr-index-preview'>PandasIndex</div><input type='checkbox' disabled/><label></label><input id='index-1e1ab467-9e9e-4719-b6cd-c5d1adf97a86' class='xr-index-data-in' type='checkbox'/><label for='index-1e1ab467-9e9e-4719-b6cd-c5d1adf97a86' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Index([10.691191383266707, 10.693246876616321, 10.695302369965935,
       10.697357863315547, 10.699413356665161, 10.701468850014775,
        10.70352434336439, 10.705579836714003, 10.707635330063615,
        10.70969082341323,
       ...
       11.671661711032407,  11.67371720438202, 11.675772697731633,
       11.677828191081247,  11.67988368443086, 11.681939177780475,
       11.683994671130089,   11.6860501644797, 11.688105657829315,
       11.690161151178929],
      dtype=&#x27;float64&#x27;, name=&#x27;qz&#x27;, length=487))</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-e214fe9e-6baf-47fd-8018-5e5a15fb36b6' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-e214fe9e-6baf-47fd-8018-5e5a15fb36b6' class='xr-section-summary'  title='Expand/collapse section'>Attributes: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'></dl></div></li></ul></div></div>




```python
proposal.r0047.cooked.images.sum('qy').plot(norm=LogNorm(1e-2, 1e1))
```




    <matplotlib.collections.QuadMesh at 0x7f278928ee40>




    
![png](output_5_1.png)
    



```python

```
