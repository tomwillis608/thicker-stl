# Figurine Base Height Heuristic

## Status

Accepted

## Context

In tabletop figurine models, the actual figure is often mounted on a disc-like base. For transformations like
thickening, the cylindrical transformation should apply only to the figurine and not the base. Manually requiring
users to input the height of the base adds complexity to the user interface and could result in errors. Therefore, we
need a heuristic to estimate the base height automatically.

## Decision

We will:

1. Use a utility to analyze the maximum radius of figurine models at various z-heights to understand the geometry of
typical figurines.
2. Generate normalized graphs of maximum radius vs. z-height for several figurines to identify common trends,
particularly regarding the base.
3. Use these data-driven insights to establish an initial heuristic for base height as a fraction of total figurine
height.
4. Integrate this heuristic into the primary application to provide a default value for base height, reducing user
input requirements.

## Utility Description

A utility was developed to assist in analyzing the geometry of STL figurines:

1. **Input:** STL files prefixed with `test_` located in a test data folder (e.g., `utils/data`).
2. **Processing:**
   - Slices the model into vertical segments.
   - Calculates the maximum radius for each slice.
   - Normalizes height and radius to produce comparable data.
3. **Output:**
   - CSV file for each STL file with normalized height and radius data.
   - Visualizations of radius vs. height graphs for qualitative analysis.

This utility provides insights into base height trends across different figurine models, enabling the derivation of a
"good-enough" heuristic.

## Rationale

- **Data-driven Approach:** Using empirical data ensures the heuristic is grounded in real-world examples,
improving reliability.
- **Automation:** By providing a default heuristic, we reduce the cognitive load on users and minimize manual errors.
- **Scalability:** The utility can be reused for future analysis of additional models to refine or validate the
heuristic.

## Consequences

### Positive

- Simplifies the user interface by automating base height estimation.
- Improves accuracy in transformations by excluding the base from calculations.
- Encourages data-driven decision-making in the application design.

### Negative

- The heuristic may not be accurate for unusual or atypical figurine models.
- Requires maintenance of the utility for further refinement of the heuristic.

## Alternatives Considered

1. **Manual Input:** Rejected due to increased complexity and potential for user error.
2. **Model-specific Configurations:** Rejected for lack of generalizability and increased setup time for users.

## Next Steps

1. Finalize and document the base height heuristic based on utility output.
2. Integrate the heuristic into the main use case of the application.
3. Provide documentation for users explaining the heuristic and its limitations.

## Related Documents

- Utility script for radius vs. height analysis
