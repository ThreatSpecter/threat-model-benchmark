# Where these came from

Six examples from [awslabs/diagram-as-code](https://github.com/awslabs/diagram-as-code), Apache 2.0, vendored
unchanged — each a YAML description of an AWS architecture and the PNG that tool renders from it.

They are here because they are the eval corpus we could not have written. The YAML names every resource and every
link, `Source` to `Target`, with an arrowhead — so components, connections **and flow direction** all have an
answer nobody had to label. And unlike a diagram we draw ourselves, these look like what a customer actually
sends: AWS icons, nested clouds, VPCs and subnets, two boxes with the same label in different subnets.

Three of the nine upstream examples are not here. `tgw-nwfw-tmpl.yaml` is a Go template rather than YAML;
`vpc-natgw.yaml` and `vpc-subnet-ec2-cfn.yaml` declare no links, so they cannot score a connection.
