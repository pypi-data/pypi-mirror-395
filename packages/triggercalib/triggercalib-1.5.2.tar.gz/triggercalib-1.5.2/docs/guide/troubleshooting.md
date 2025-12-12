# Troubleshooting

Here the most common problems and questions about TriggerCalib are collected with their answers.
Frequently asked questions are added below as and when they are asked.

If your question is not answered below or if you would like to discuss it in more detail then you are welcome to join the [TriggerCalib Mattermost channel](https://mattermost.web.cern.ch/lhcb/channels/triggercalib).

## Frequently asked questions

!!! note ""

    !!! question
        I'm receiving an_ ``INFO`` message, " ``Bin contains more passing events than total events (efficiency > 1), setting N(passing) to N(total)``".
        Is this cause for concern?
    
    In short, usually no.
    This message arises for bins with efficiencies close to one, wherein statistical fluctuations in the background mitigation cause the numerator of the efficiency to become larger than the denominator, an unphysical effect.
    To handle this, the numerator is set to the same value as the denominator, i.e., the efficiency is set to 1.
    This is expected to negligibly effect the efficiencies; however, if this message is appearing frequently, this is typically a sign that you have many empty bins and should consider a coarser binning scheme (fewer bins).


!!! info 
    More questions will be added as they are asked.