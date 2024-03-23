# Mutate Mate

## _Kubernetes Mutation Webhook İplementation for secret, resource management_

At our company we are using a tool for Data Science operations. This tool has flaws. To fix that we thought using Mutating Web Hooks is a great option.

This API's kubernetes project will have multiple secret definitons in that project.
At the webhook call, first we will look for defitions. Definitions has key words with hastags. These will determine which secrets will ve injected to Notebook or Pipeline CRDs.
As a second step, if the call is for Elyra Pipelines, we will get the limitations for project and apply the same settings to Elyra Pipelines.

This way secrets will be auto assingned and will be at single namespace.
Elyra pipelines is resource and secrets will be installed automatically with no manuel operation.

If you have same problem, Ihope this will solve your problem too.
