## Glossary

For rapid reference, here's a short list of the vernacular of Nx5d's
core concepts:

#### Frame
A single measurement unit encompassing data from *all* sources relevant
to the experiment. Frames are the smallest building blocks of data.

#### Scan
A collection of frames, typically representing a measurement sequence.
Scans are the basic unit of processing.

#### Scan Type
A classification that describes the purpose or "nature" of a scan
(e.g. calibration scan, measurement scan). Scan types can influence
which spice values or recipes apply.

#### Proposal
A grouping of scans under a scientific project or experiment. Proposals
provide scope for managing metadata and results.

#### (Data) Processing
Applying the entirety of data transformations and computations needed
to extract knowledge (e.g. publications, long-term storage of insight
etc).

#### Cooking
Executing algorithms to transform raw scans into processed data
(processing step 1 of 2, typically focused on engineering
transformations).

#### Analyzing
When used in contrast to *cooking*: interpreting and evaluating the
processed data (processing step 2 of 2, focused on the science).
Also used interchangably with *processing* when the two-step
process is not the focus of discussion.

#### Recipe
Algorithm or API call that performs the *cooking* step, i.e. the
mostly-engineering transformation required for data processing.
Typically, a *recipe* requires *raw data* and *spice* to produce
*cooked data*.

#### Spice
Metadata used for processing, predominantly for the *cooking* part.

#### Seeding (Spice)
The act of providing initial spice values (defaults,
measurement-derived, or user input) to the proposal.

### Updating (Spice)
Changing spice values after seeding. Updates allow iterative 
refining of parameters in a non-linear / loop-based processing
workflow.

#### Anchor (Spice) 
A propagation boundary for spice *updates* in the scan list.
Anchors ensure that later updates affect only a limited number
of consecutive scans.

### View Point (Spice)
The perspective from which spice values are retrieved. Different
view points may yield different values, depending on updates and
anchors.

#### Branch (Spice)
The entirety of the current and historical values of a spice type
between two anchor points, or an anchor point and one end of 
the scan list it applies to.

#### Spice Type
Several spice keys bound together under a common name for ease
of addressing.
