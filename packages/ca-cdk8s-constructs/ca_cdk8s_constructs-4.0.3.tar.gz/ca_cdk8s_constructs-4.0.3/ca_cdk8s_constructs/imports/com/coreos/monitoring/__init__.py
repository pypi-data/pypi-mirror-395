from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import cdk8s as _cdk8s_d3d9af27
import constructs as _constructs_77d1e7e8


class Probe(
    _cdk8s_d3d9af27.ApiObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="comcoreosmonitoring.Probe",
):
    '''The ``Probe`` custom resource definition (CRD) defines how to scrape metrics from prober exporters such as the `blackbox exporter <https://github.com/prometheus/blackbox_exporter>`_.

    The ``Probe`` resource needs 2 pieces of information:
    The list of probed addresses which can be defined statically or by discovering Kubernetes Ingress objects.
    The prober which exposes the availability of probed endpoints (over various protocols such HTTP, TCP, ICMP, ...) as Prometheus metrics.

    ``Prometheus`` and ``PrometheusAgent`` objects select ``Probe`` objects using label and namespace selectors.

    :schema: Probe
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        spec: typing.Union["ProbeSpec", typing.Dict[builtins.str, typing.Any]],
        metadata: typing.Optional[typing.Union[_cdk8s_d3d9af27.ApiObjectMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Defines a "Probe" API object.

        :param scope: the scope in which to define this object.
        :param id: a scope-local name for the object.
        :param spec: spec defines the specification of desired Ingress selection for target discovery by Prometheus.
        :param metadata: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d431973747a4e312d98bbfc6c85e22bfcc072205d8b977840cdd34994c446c3b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ProbeProps(spec=spec, metadata=metadata)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="manifest")
    @builtins.classmethod
    def manifest(
        cls,
        *,
        spec: typing.Union["ProbeSpec", typing.Dict[builtins.str, typing.Any]],
        metadata: typing.Optional[typing.Union[_cdk8s_d3d9af27.ApiObjectMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> typing.Any:
        '''Renders a Kubernetes manifest for "Probe".

        This can be used to inline resource manifests inside other objects (e.g. as templates).

        :param spec: spec defines the specification of desired Ingress selection for target discovery by Prometheus.
        :param metadata: 
        '''
        props = ProbeProps(spec=spec, metadata=metadata)

        return typing.cast(typing.Any, jsii.sinvoke(cls, "manifest", [props]))

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.Any:
        '''Renders the object to Kubernetes JSON.'''
        return typing.cast(typing.Any, jsii.invoke(self, "toJson", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GVK")
    def GVK(cls) -> _cdk8s_d3d9af27.GroupVersionKind:
        '''Returns the apiVersion and kind for "Probe".'''
        return typing.cast(_cdk8s_d3d9af27.GroupVersionKind, jsii.sget(cls, "GVK"))


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeProps",
    jsii_struct_bases=[],
    name_mapping={"spec": "spec", "metadata": "metadata"},
)
class ProbeProps:
    def __init__(
        self,
        *,
        spec: typing.Union["ProbeSpec", typing.Dict[builtins.str, typing.Any]],
        metadata: typing.Optional[typing.Union[_cdk8s_d3d9af27.ApiObjectMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''The ``Probe`` custom resource definition (CRD) defines how to scrape metrics from prober exporters such as the `blackbox exporter <https://github.com/prometheus/blackbox_exporter>`_.

        The ``Probe`` resource needs 2 pieces of information:

        - The list of probed addresses which can be defined statically or by discovering Kubernetes Ingress objects.
        - The prober which exposes the availability of probed endpoints (over various protocols such HTTP, TCP, ICMP, ...) as Prometheus metrics.

        ``Prometheus`` and ``PrometheusAgent`` objects select ``Probe`` objects using label and namespace selectors.

        :param spec: spec defines the specification of desired Ingress selection for target discovery by Prometheus.
        :param metadata: 

        :schema: Probe
        '''
        if isinstance(spec, dict):
            spec = ProbeSpec(**spec)
        if isinstance(metadata, dict):
            metadata = _cdk8s_d3d9af27.ApiObjectMetadata(**metadata)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dfdb1f8ee121f58da1f22691f2f6aa14bc10cbb8707eef9c91e85264c784a46)
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "spec": spec,
        }
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def spec(self) -> "ProbeSpec":
        '''spec defines the specification of desired Ingress selection for target discovery by Prometheus.

        :schema: Probe#spec
        '''
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("ProbeSpec", result)

    @builtins.property
    def metadata(self) -> typing.Optional[_cdk8s_d3d9af27.ApiObjectMetadata]:
        '''
        :schema: Probe#metadata
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[_cdk8s_d3d9af27.ApiObjectMetadata], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpec",
    jsii_struct_bases=[],
    name_mapping={
        "authorization": "authorization",
        "basic_auth": "basicAuth",
        "bearer_token_secret": "bearerTokenSecret",
        "convert_classic_histograms_to_nhcb": "convertClassicHistogramsToNhcb",
        "enable_http2": "enableHttp2",
        "fallback_scrape_protocol": "fallbackScrapeProtocol",
        "follow_redirects": "followRedirects",
        "interval": "interval",
        "job_name": "jobName",
        "keep_dropped_targets": "keepDroppedTargets",
        "label_limit": "labelLimit",
        "label_name_length_limit": "labelNameLengthLimit",
        "label_value_length_limit": "labelValueLengthLimit",
        "metric_relabelings": "metricRelabelings",
        "module": "module",
        "native_histogram_bucket_limit": "nativeHistogramBucketLimit",
        "native_histogram_min_bucket_factor": "nativeHistogramMinBucketFactor",
        "oauth2": "oauth2",
        "params": "params",
        "prober": "prober",
        "sample_limit": "sampleLimit",
        "scrape_class": "scrapeClass",
        "scrape_classic_histograms": "scrapeClassicHistograms",
        "scrape_protocols": "scrapeProtocols",
        "scrape_timeout": "scrapeTimeout",
        "target_limit": "targetLimit",
        "targets": "targets",
        "tls_config": "tlsConfig",
    },
)
class ProbeSpec:
    def __init__(
        self,
        *,
        authorization: typing.Optional[typing.Union["ProbeSpecAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        basic_auth: typing.Optional[typing.Union["ProbeSpecBasicAuth", typing.Dict[builtins.str, typing.Any]]] = None,
        bearer_token_secret: typing.Optional[typing.Union["ProbeSpecBearerTokenSecret", typing.Dict[builtins.str, typing.Any]]] = None,
        convert_classic_histograms_to_nhcb: typing.Optional[builtins.bool] = None,
        enable_http2: typing.Optional[builtins.bool] = None,
        fallback_scrape_protocol: typing.Optional["ProbeSpecFallbackScrapeProtocol"] = None,
        follow_redirects: typing.Optional[builtins.bool] = None,
        interval: typing.Optional[builtins.str] = None,
        job_name: typing.Optional[builtins.str] = None,
        keep_dropped_targets: typing.Optional[jsii.Number] = None,
        label_limit: typing.Optional[jsii.Number] = None,
        label_name_length_limit: typing.Optional[jsii.Number] = None,
        label_value_length_limit: typing.Optional[jsii.Number] = None,
        metric_relabelings: typing.Optional[typing.Sequence[typing.Union["ProbeSpecMetricRelabelings", typing.Dict[builtins.str, typing.Any]]]] = None,
        module: typing.Optional[builtins.str] = None,
        native_histogram_bucket_limit: typing.Optional[jsii.Number] = None,
        native_histogram_min_bucket_factor: typing.Optional["ProbeSpecNativeHistogramMinBucketFactor"] = None,
        oauth2: typing.Optional[typing.Union["ProbeSpecOauth2", typing.Dict[builtins.str, typing.Any]]] = None,
        params: typing.Optional[typing.Sequence[typing.Union["ProbeSpecParams", typing.Dict[builtins.str, typing.Any]]]] = None,
        prober: typing.Optional[typing.Union["ProbeSpecProber", typing.Dict[builtins.str, typing.Any]]] = None,
        sample_limit: typing.Optional[jsii.Number] = None,
        scrape_class: typing.Optional[builtins.str] = None,
        scrape_classic_histograms: typing.Optional[builtins.bool] = None,
        scrape_protocols: typing.Optional[typing.Sequence["ProbeSpecScrapeProtocols"]] = None,
        scrape_timeout: typing.Optional[builtins.str] = None,
        target_limit: typing.Optional[jsii.Number] = None,
        targets: typing.Optional[typing.Union["ProbeSpecTargets", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_config: typing.Optional[typing.Union["ProbeSpecTlsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''spec defines the specification of desired Ingress selection for target discovery by Prometheus.

        :param authorization: authorization configures the Authorization header credentials used by the client. Cannot be set at the same time as ``basicAuth``, ``bearerTokenSecret`` or ``oauth2``.
        :param basic_auth: basicAuth defines the Basic Authentication credentials used by the client. Cannot be set at the same time as ``authorization``, ``bearerTokenSecret`` or ``oauth2``.
        :param bearer_token_secret: bearerTokenSecret defines a key of a Secret containing the bearer token used by the client for authentication. The secret needs to be in the same namespace as the custom resource and readable by the Prometheus Operator. Cannot be set at the same time as ``authorization``, ``basicAuth`` or ``oauth2``. Deprecated: use ``authorization`` instead.
        :param convert_classic_histograms_to_nhcb: convertClassicHistogramsToNHCB defines whether to convert all scraped classic histograms into a native histogram with custom buckets. It requires Prometheus >= v3.0.0.
        :param enable_http2: enableHttp2 can be used to disable HTTP2.
        :param fallback_scrape_protocol: fallbackScrapeProtocol defines the protocol to use if a scrape returns blank, unparseable, or otherwise invalid Content-Type. It requires Prometheus >= v3.0.0.
        :param follow_redirects: followRedirects defines whether the client should follow HTTP 3xx redirects.
        :param interval: interval at which targets are probed using the configured prober. If not specified Prometheus' global scrape interval is used.
        :param job_name: jobName assigned to scraped metrics by default.
        :param keep_dropped_targets: keepDroppedTargets defines the per-scrape limit on the number of targets dropped by relabeling that will be kept in memory. 0 means no limit. It requires Prometheus >= v2.47.0.
        :param label_limit: labelLimit defines the per-scrape limit on number of labels that will be accepted for a sample. Only valid in Prometheus versions 2.27.0 and newer.
        :param label_name_length_limit: labelNameLengthLimit defines the per-scrape limit on length of labels name that will be accepted for a sample. Only valid in Prometheus versions 2.27.0 and newer.
        :param label_value_length_limit: labelValueLengthLimit defines the per-scrape limit on length of labels value that will be accepted for a sample. Only valid in Prometheus versions 2.27.0 and newer.
        :param metric_relabelings: metricRelabelings defines the RelabelConfig to apply to samples before ingestion.
        :param module: module to use for probing specifying how to probe the target. Example module configuring in the blackbox exporter: https://github.com/prometheus/blackbox_exporter/blob/master/example.yml
        :param native_histogram_bucket_limit: nativeHistogramBucketLimit defines ff there are more than this many buckets in a native histogram, buckets will be merged to stay within the limit. It requires Prometheus >= v2.45.0.
        :param native_histogram_min_bucket_factor: nativeHistogramMinBucketFactor defines if the growth factor of one bucket to the next is smaller than this, buckets will be merged to increase the factor sufficiently. It requires Prometheus >= v2.50.0.
        :param oauth2: oauth2 defines the OAuth2 settings used by the client. It requires Prometheus >= 2.27.0. Cannot be set at the same time as ``authorization``, ``basicAuth`` or ``bearerTokenSecret``.
        :param params: params defines the list of HTTP query parameters for the scrape. Please note that the ``.spec.module`` field takes precedence over the ``module`` parameter from this list when both are defined. The module name must be added using Module under ProbeSpec.
        :param prober: prober defines the specification for the prober to use for probing targets. The prober.URL parameter is required. Targets cannot be probed if left empty.
        :param sample_limit: sampleLimit defines per-scrape limit on number of scraped samples that will be accepted.
        :param scrape_class: scrapeClass defines the scrape class to apply.
        :param scrape_classic_histograms: scrapeClassicHistograms defines whether to scrape a classic histogram that is also exposed as a native histogram. It requires Prometheus >= v2.45.0. Notice: ``scrapeClassicHistograms`` corresponds to the ``always_scrape_classic_histograms`` field in the Prometheus configuration.
        :param scrape_protocols: scrapeProtocols defines the protocols to negotiate during a scrape. It tells clients the protocols supported by Prometheus in order of preference (from most to least preferred). If unset, Prometheus uses its default value. It requires Prometheus >= v2.49.0.
        :param scrape_timeout: scrapeTimeout defines the timeout for scraping metrics from the Prometheus exporter. If not specified, the Prometheus global scrape timeout is used. The value cannot be greater than the scrape interval otherwise the operator will reject the resource.
        :param target_limit: targetLimit defines a limit on the number of scraped targets that will be accepted.
        :param targets: targets defines a set of static or dynamically discovered targets to probe.
        :param tls_config: tlsConfig defines the TLS configuration used by the client.

        :schema: ProbeSpec
        '''
        if isinstance(authorization, dict):
            authorization = ProbeSpecAuthorization(**authorization)
        if isinstance(basic_auth, dict):
            basic_auth = ProbeSpecBasicAuth(**basic_auth)
        if isinstance(bearer_token_secret, dict):
            bearer_token_secret = ProbeSpecBearerTokenSecret(**bearer_token_secret)
        if isinstance(oauth2, dict):
            oauth2 = ProbeSpecOauth2(**oauth2)
        if isinstance(prober, dict):
            prober = ProbeSpecProber(**prober)
        if isinstance(targets, dict):
            targets = ProbeSpecTargets(**targets)
        if isinstance(tls_config, dict):
            tls_config = ProbeSpecTlsConfig(**tls_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4da9453333edbc627c631d6c0043f58d9dc9b96a470aabc5bda67f045c750a88)
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument bearer_token_secret", value=bearer_token_secret, expected_type=type_hints["bearer_token_secret"])
            check_type(argname="argument convert_classic_histograms_to_nhcb", value=convert_classic_histograms_to_nhcb, expected_type=type_hints["convert_classic_histograms_to_nhcb"])
            check_type(argname="argument enable_http2", value=enable_http2, expected_type=type_hints["enable_http2"])
            check_type(argname="argument fallback_scrape_protocol", value=fallback_scrape_protocol, expected_type=type_hints["fallback_scrape_protocol"])
            check_type(argname="argument follow_redirects", value=follow_redirects, expected_type=type_hints["follow_redirects"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument keep_dropped_targets", value=keep_dropped_targets, expected_type=type_hints["keep_dropped_targets"])
            check_type(argname="argument label_limit", value=label_limit, expected_type=type_hints["label_limit"])
            check_type(argname="argument label_name_length_limit", value=label_name_length_limit, expected_type=type_hints["label_name_length_limit"])
            check_type(argname="argument label_value_length_limit", value=label_value_length_limit, expected_type=type_hints["label_value_length_limit"])
            check_type(argname="argument metric_relabelings", value=metric_relabelings, expected_type=type_hints["metric_relabelings"])
            check_type(argname="argument module", value=module, expected_type=type_hints["module"])
            check_type(argname="argument native_histogram_bucket_limit", value=native_histogram_bucket_limit, expected_type=type_hints["native_histogram_bucket_limit"])
            check_type(argname="argument native_histogram_min_bucket_factor", value=native_histogram_min_bucket_factor, expected_type=type_hints["native_histogram_min_bucket_factor"])
            check_type(argname="argument oauth2", value=oauth2, expected_type=type_hints["oauth2"])
            check_type(argname="argument params", value=params, expected_type=type_hints["params"])
            check_type(argname="argument prober", value=prober, expected_type=type_hints["prober"])
            check_type(argname="argument sample_limit", value=sample_limit, expected_type=type_hints["sample_limit"])
            check_type(argname="argument scrape_class", value=scrape_class, expected_type=type_hints["scrape_class"])
            check_type(argname="argument scrape_classic_histograms", value=scrape_classic_histograms, expected_type=type_hints["scrape_classic_histograms"])
            check_type(argname="argument scrape_protocols", value=scrape_protocols, expected_type=type_hints["scrape_protocols"])
            check_type(argname="argument scrape_timeout", value=scrape_timeout, expected_type=type_hints["scrape_timeout"])
            check_type(argname="argument target_limit", value=target_limit, expected_type=type_hints["target_limit"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument tls_config", value=tls_config, expected_type=type_hints["tls_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorization is not None:
            self._values["authorization"] = authorization
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if bearer_token_secret is not None:
            self._values["bearer_token_secret"] = bearer_token_secret
        if convert_classic_histograms_to_nhcb is not None:
            self._values["convert_classic_histograms_to_nhcb"] = convert_classic_histograms_to_nhcb
        if enable_http2 is not None:
            self._values["enable_http2"] = enable_http2
        if fallback_scrape_protocol is not None:
            self._values["fallback_scrape_protocol"] = fallback_scrape_protocol
        if follow_redirects is not None:
            self._values["follow_redirects"] = follow_redirects
        if interval is not None:
            self._values["interval"] = interval
        if job_name is not None:
            self._values["job_name"] = job_name
        if keep_dropped_targets is not None:
            self._values["keep_dropped_targets"] = keep_dropped_targets
        if label_limit is not None:
            self._values["label_limit"] = label_limit
        if label_name_length_limit is not None:
            self._values["label_name_length_limit"] = label_name_length_limit
        if label_value_length_limit is not None:
            self._values["label_value_length_limit"] = label_value_length_limit
        if metric_relabelings is not None:
            self._values["metric_relabelings"] = metric_relabelings
        if module is not None:
            self._values["module"] = module
        if native_histogram_bucket_limit is not None:
            self._values["native_histogram_bucket_limit"] = native_histogram_bucket_limit
        if native_histogram_min_bucket_factor is not None:
            self._values["native_histogram_min_bucket_factor"] = native_histogram_min_bucket_factor
        if oauth2 is not None:
            self._values["oauth2"] = oauth2
        if params is not None:
            self._values["params"] = params
        if prober is not None:
            self._values["prober"] = prober
        if sample_limit is not None:
            self._values["sample_limit"] = sample_limit
        if scrape_class is not None:
            self._values["scrape_class"] = scrape_class
        if scrape_classic_histograms is not None:
            self._values["scrape_classic_histograms"] = scrape_classic_histograms
        if scrape_protocols is not None:
            self._values["scrape_protocols"] = scrape_protocols
        if scrape_timeout is not None:
            self._values["scrape_timeout"] = scrape_timeout
        if target_limit is not None:
            self._values["target_limit"] = target_limit
        if targets is not None:
            self._values["targets"] = targets
        if tls_config is not None:
            self._values["tls_config"] = tls_config

    @builtins.property
    def authorization(self) -> typing.Optional["ProbeSpecAuthorization"]:
        '''authorization configures the Authorization header credentials used by the client.

        Cannot be set at the same time as ``basicAuth``, ``bearerTokenSecret`` or ``oauth2``.

        :schema: ProbeSpec#authorization
        '''
        result = self._values.get("authorization")
        return typing.cast(typing.Optional["ProbeSpecAuthorization"], result)

    @builtins.property
    def basic_auth(self) -> typing.Optional["ProbeSpecBasicAuth"]:
        '''basicAuth defines the Basic Authentication credentials used by the client.

        Cannot be set at the same time as ``authorization``, ``bearerTokenSecret`` or ``oauth2``.

        :schema: ProbeSpec#basicAuth
        '''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional["ProbeSpecBasicAuth"], result)

    @builtins.property
    def bearer_token_secret(self) -> typing.Optional["ProbeSpecBearerTokenSecret"]:
        '''bearerTokenSecret defines a key of a Secret containing the bearer token used by the client for authentication.

        The secret needs to be in the
        same namespace as the custom resource and readable by the Prometheus
        Operator.

        Cannot be set at the same time as ``authorization``, ``basicAuth`` or ``oauth2``.

        Deprecated: use ``authorization`` instead.

        :schema: ProbeSpec#bearerTokenSecret
        '''
        result = self._values.get("bearer_token_secret")
        return typing.cast(typing.Optional["ProbeSpecBearerTokenSecret"], result)

    @builtins.property
    def convert_classic_histograms_to_nhcb(self) -> typing.Optional[builtins.bool]:
        '''convertClassicHistogramsToNHCB defines whether to convert all scraped classic histograms into a native histogram with custom buckets.

        It requires Prometheus >= v3.0.0.

        :schema: ProbeSpec#convertClassicHistogramsToNHCB
        '''
        result = self._values.get("convert_classic_histograms_to_nhcb")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_http2(self) -> typing.Optional[builtins.bool]:
        '''enableHttp2 can be used to disable HTTP2.

        :schema: ProbeSpec#enableHttp2
        '''
        result = self._values.get("enable_http2")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def fallback_scrape_protocol(
        self,
    ) -> typing.Optional["ProbeSpecFallbackScrapeProtocol"]:
        '''fallbackScrapeProtocol defines the protocol to use if a scrape returns blank, unparseable, or otherwise invalid Content-Type.

        It requires Prometheus >= v3.0.0.

        :schema: ProbeSpec#fallbackScrapeProtocol
        '''
        result = self._values.get("fallback_scrape_protocol")
        return typing.cast(typing.Optional["ProbeSpecFallbackScrapeProtocol"], result)

    @builtins.property
    def follow_redirects(self) -> typing.Optional[builtins.bool]:
        '''followRedirects defines whether the client should follow HTTP 3xx redirects.

        :schema: ProbeSpec#followRedirects
        '''
        result = self._values.get("follow_redirects")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def interval(self) -> typing.Optional[builtins.str]:
        '''interval at which targets are probed using the configured prober.

        If not specified Prometheus' global scrape interval is used.

        :schema: ProbeSpec#interval
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''jobName assigned to scraped metrics by default.

        :schema: ProbeSpec#jobName
        '''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keep_dropped_targets(self) -> typing.Optional[jsii.Number]:
        '''keepDroppedTargets defines the per-scrape limit on the number of targets dropped by relabeling that will be kept in memory.

        0 means no limit.

        It requires Prometheus >= v2.47.0.

        :schema: ProbeSpec#keepDroppedTargets
        '''
        result = self._values.get("keep_dropped_targets")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def label_limit(self) -> typing.Optional[jsii.Number]:
        '''labelLimit defines the per-scrape limit on number of labels that will be accepted for a sample.

        Only valid in Prometheus versions 2.27.0 and newer.

        :schema: ProbeSpec#labelLimit
        '''
        result = self._values.get("label_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def label_name_length_limit(self) -> typing.Optional[jsii.Number]:
        '''labelNameLengthLimit defines the per-scrape limit on length of labels name that will be accepted for a sample.

        Only valid in Prometheus versions 2.27.0 and newer.

        :schema: ProbeSpec#labelNameLengthLimit
        '''
        result = self._values.get("label_name_length_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def label_value_length_limit(self) -> typing.Optional[jsii.Number]:
        '''labelValueLengthLimit defines the per-scrape limit on length of labels value that will be accepted for a sample.

        Only valid in Prometheus versions 2.27.0 and newer.

        :schema: ProbeSpec#labelValueLengthLimit
        '''
        result = self._values.get("label_value_length_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metric_relabelings(
        self,
    ) -> typing.Optional[typing.List["ProbeSpecMetricRelabelings"]]:
        '''metricRelabelings defines the RelabelConfig to apply to samples before ingestion.

        :schema: ProbeSpec#metricRelabelings
        '''
        result = self._values.get("metric_relabelings")
        return typing.cast(typing.Optional[typing.List["ProbeSpecMetricRelabelings"]], result)

    @builtins.property
    def module(self) -> typing.Optional[builtins.str]:
        '''module to use for probing specifying how to probe the target.

        Example module configuring in the blackbox exporter:
        https://github.com/prometheus/blackbox_exporter/blob/master/example.yml

        :schema: ProbeSpec#module
        '''
        result = self._values.get("module")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def native_histogram_bucket_limit(self) -> typing.Optional[jsii.Number]:
        '''nativeHistogramBucketLimit defines ff there are more than this many buckets in a native histogram, buckets will be merged to stay within the limit.

        It requires Prometheus >= v2.45.0.

        :schema: ProbeSpec#nativeHistogramBucketLimit
        '''
        result = self._values.get("native_histogram_bucket_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def native_histogram_min_bucket_factor(
        self,
    ) -> typing.Optional["ProbeSpecNativeHistogramMinBucketFactor"]:
        '''nativeHistogramMinBucketFactor defines if the growth factor of one bucket to the next is smaller than this, buckets will be merged to increase the factor sufficiently.

        It requires Prometheus >= v2.50.0.

        :schema: ProbeSpec#nativeHistogramMinBucketFactor
        '''
        result = self._values.get("native_histogram_min_bucket_factor")
        return typing.cast(typing.Optional["ProbeSpecNativeHistogramMinBucketFactor"], result)

    @builtins.property
    def oauth2(self) -> typing.Optional["ProbeSpecOauth2"]:
        '''oauth2 defines the OAuth2 settings used by the client.

        It requires Prometheus >= 2.27.0.

        Cannot be set at the same time as ``authorization``, ``basicAuth`` or ``bearerTokenSecret``.

        :schema: ProbeSpec#oauth2
        '''
        result = self._values.get("oauth2")
        return typing.cast(typing.Optional["ProbeSpecOauth2"], result)

    @builtins.property
    def params(self) -> typing.Optional[typing.List["ProbeSpecParams"]]:
        '''params defines the list of HTTP query parameters for the scrape.

        Please note that the ``.spec.module`` field takes precedence over the ``module`` parameter from this list when both are defined.
        The module name must be added using Module under ProbeSpec.

        :schema: ProbeSpec#params
        '''
        result = self._values.get("params")
        return typing.cast(typing.Optional[typing.List["ProbeSpecParams"]], result)

    @builtins.property
    def prober(self) -> typing.Optional["ProbeSpecProber"]:
        '''prober defines the specification for the prober to use for probing targets.

        The prober.URL parameter is required. Targets cannot be probed if left empty.

        :schema: ProbeSpec#prober
        '''
        result = self._values.get("prober")
        return typing.cast(typing.Optional["ProbeSpecProber"], result)

    @builtins.property
    def sample_limit(self) -> typing.Optional[jsii.Number]:
        '''sampleLimit defines per-scrape limit on number of scraped samples that will be accepted.

        :schema: ProbeSpec#sampleLimit
        '''
        result = self._values.get("sample_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scrape_class(self) -> typing.Optional[builtins.str]:
        '''scrapeClass defines the scrape class to apply.

        :schema: ProbeSpec#scrapeClass
        '''
        result = self._values.get("scrape_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scrape_classic_histograms(self) -> typing.Optional[builtins.bool]:
        '''scrapeClassicHistograms defines whether to scrape a classic histogram that is also exposed as a native histogram.

        It requires Prometheus >= v2.45.0.

        Notice: ``scrapeClassicHistograms`` corresponds to the ``always_scrape_classic_histograms`` field in the Prometheus configuration.

        :schema: ProbeSpec#scrapeClassicHistograms
        '''
        result = self._values.get("scrape_classic_histograms")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def scrape_protocols(
        self,
    ) -> typing.Optional[typing.List["ProbeSpecScrapeProtocols"]]:
        '''scrapeProtocols defines the protocols to negotiate during a scrape.

        It tells clients the
        protocols supported by Prometheus in order of preference (from most to least preferred).

        If unset, Prometheus uses its default value.

        It requires Prometheus >= v2.49.0.

        :schema: ProbeSpec#scrapeProtocols
        '''
        result = self._values.get("scrape_protocols")
        return typing.cast(typing.Optional[typing.List["ProbeSpecScrapeProtocols"]], result)

    @builtins.property
    def scrape_timeout(self) -> typing.Optional[builtins.str]:
        '''scrapeTimeout defines the timeout for scraping metrics from the Prometheus exporter.

        If not specified, the Prometheus global scrape timeout is used.
        The value cannot be greater than the scrape interval otherwise the operator will reject the resource.

        :schema: ProbeSpec#scrapeTimeout
        '''
        result = self._values.get("scrape_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_limit(self) -> typing.Optional[jsii.Number]:
        '''targetLimit defines a limit on the number of scraped targets that will be accepted.

        :schema: ProbeSpec#targetLimit
        '''
        result = self._values.get("target_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def targets(self) -> typing.Optional["ProbeSpecTargets"]:
        '''targets defines a set of static or dynamically discovered targets to probe.

        :schema: ProbeSpec#targets
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional["ProbeSpecTargets"], result)

    @builtins.property
    def tls_config(self) -> typing.Optional["ProbeSpecTlsConfig"]:
        '''tlsConfig defines the TLS configuration used by the client.

        :schema: ProbeSpec#tlsConfig
        '''
        result = self._values.get("tls_config")
        return typing.cast(typing.Optional["ProbeSpecTlsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecAuthorization",
    jsii_struct_bases=[],
    name_mapping={"credentials": "credentials", "type": "type"},
)
class ProbeSpecAuthorization:
    def __init__(
        self,
        *,
        credentials: typing.Optional[typing.Union["ProbeSpecAuthorizationCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''authorization configures the Authorization header credentials used by the client.

        Cannot be set at the same time as ``basicAuth``, ``bearerTokenSecret`` or ``oauth2``.

        :param credentials: credentials defines a key of a Secret in the namespace that contains the credentials for authentication.
        :param type: type defines the authentication type. The value is case-insensitive. "Basic" is not a supported value. Default: "Bearer"

        :schema: ProbeSpecAuthorization
        '''
        if isinstance(credentials, dict):
            credentials = ProbeSpecAuthorizationCredentials(**credentials)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53119ace9a7835b3dc700fa87720e6dd11a003f2a7fc4457715e90440952103f)
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if credentials is not None:
            self._values["credentials"] = credentials
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def credentials(self) -> typing.Optional["ProbeSpecAuthorizationCredentials"]:
        '''credentials defines a key of a Secret in the namespace that contains the credentials for authentication.

        :schema: ProbeSpecAuthorization#credentials
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional["ProbeSpecAuthorizationCredentials"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''type defines the authentication type. The value is case-insensitive.

        "Basic" is not a supported value.

        Default: "Bearer"

        :schema: ProbeSpecAuthorization#type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecAuthorizationCredentials",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecAuthorizationCredentials:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''credentials defines a key of a Secret in the namespace that contains the credentials for authentication.

        :param key: The key of the secret to select from. Must be a valid secret key.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecAuthorizationCredentials
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__517b59dcdc17adab6d92c779136e1af970c3610952d33993c1951b07b2b438c3)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the secret to select from.

        Must be a valid secret key.

        :schema: ProbeSpecAuthorizationCredentials#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecAuthorizationCredentials#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecAuthorizationCredentials#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecAuthorizationCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecBasicAuth",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class ProbeSpecBasicAuth:
    def __init__(
        self,
        *,
        password: typing.Optional[typing.Union["ProbeSpecBasicAuthPassword", typing.Dict[builtins.str, typing.Any]]] = None,
        username: typing.Optional[typing.Union["ProbeSpecBasicAuthUsername", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''basicAuth defines the Basic Authentication credentials used by the client.

        Cannot be set at the same time as ``authorization``, ``bearerTokenSecret`` or ``oauth2``.

        :param password: password defines a key of a Secret containing the password for authentication.
        :param username: username defines a key of a Secret containing the username for authentication.

        :schema: ProbeSpecBasicAuth
        '''
        if isinstance(password, dict):
            password = ProbeSpecBasicAuthPassword(**password)
        if isinstance(username, dict):
            username = ProbeSpecBasicAuthUsername(**username)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4768e0bb103c7f5c864a395f4c7c73437a4bb218bd61f88ce14258902c233463)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def password(self) -> typing.Optional["ProbeSpecBasicAuthPassword"]:
        '''password defines a key of a Secret containing the password for authentication.

        :schema: ProbeSpecBasicAuth#password
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional["ProbeSpecBasicAuthPassword"], result)

    @builtins.property
    def username(self) -> typing.Optional["ProbeSpecBasicAuthUsername"]:
        '''username defines a key of a Secret containing the username for authentication.

        :schema: ProbeSpecBasicAuth#username
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional["ProbeSpecBasicAuthUsername"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecBasicAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecBasicAuthPassword",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecBasicAuthPassword:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''password defines a key of a Secret containing the password for authentication.

        :param key: The key of the secret to select from. Must be a valid secret key.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecBasicAuthPassword
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__780ef3df5e7ff3c36cd640940223f69d3ed0f61e6cccb5a5fef1039879162e68)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the secret to select from.

        Must be a valid secret key.

        :schema: ProbeSpecBasicAuthPassword#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecBasicAuthPassword#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecBasicAuthPassword#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecBasicAuthPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecBasicAuthUsername",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecBasicAuthUsername:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''username defines a key of a Secret containing the username for authentication.

        :param key: The key of the secret to select from. Must be a valid secret key.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecBasicAuthUsername
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e43c9454cc4ce860c775eb76aaf3e59407bfad140ff617ddc8b81d03f12957f)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the secret to select from.

        Must be a valid secret key.

        :schema: ProbeSpecBasicAuthUsername#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecBasicAuthUsername#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecBasicAuthUsername#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecBasicAuthUsername(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecBearerTokenSecret",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecBearerTokenSecret:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''bearerTokenSecret defines a key of a Secret containing the bearer token used by the client for authentication.

        The secret needs to be in the
        same namespace as the custom resource and readable by the Prometheus
        Operator.

        Cannot be set at the same time as ``authorization``, ``basicAuth`` or ``oauth2``.

        Deprecated: use ``authorization`` instead.

        :param key: The key of the secret to select from. Must be a valid secret key.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecBearerTokenSecret
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a16eb69c2dbd20d71a7eeb9b0e7066b3f1c11e88f44ff60ef5064326b2fc6e89)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the secret to select from.

        Must be a valid secret key.

        :schema: ProbeSpecBearerTokenSecret#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecBearerTokenSecret#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecBearerTokenSecret#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecBearerTokenSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="comcoreosmonitoring.ProbeSpecFallbackScrapeProtocol")
class ProbeSpecFallbackScrapeProtocol(enum.Enum):
    '''fallbackScrapeProtocol defines the protocol to use if a scrape returns blank, unparseable, or otherwise invalid Content-Type.

    It requires Prometheus >= v3.0.0.

    :schema: ProbeSpecFallbackScrapeProtocol
    '''

    PROMETHEUS_PROTO = "PROMETHEUS_PROTO"
    '''PrometheusProto.'''
    OPEN_METRICS_TEXT0_0_1 = "OPEN_METRICS_TEXT0_0_1"
    '''OpenMetricsText0.0.1.'''
    OPEN_METRICS_TEXT1_0_0 = "OPEN_METRICS_TEXT1_0_0"
    '''OpenMetricsText1.0.0.'''
    PROMETHEUS_TEXT0_0_4 = "PROMETHEUS_TEXT0_0_4"
    '''PrometheusText0.0.4.'''
    PROMETHEUS_TEXT1_0_0 = "PROMETHEUS_TEXT1_0_0"
    '''PrometheusText1.0.0.'''


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecMetricRelabelings",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "modulus": "modulus",
        "regex": "regex",
        "replacement": "replacement",
        "separator": "separator",
        "source_labels": "sourceLabels",
        "target_label": "targetLabel",
    },
)
class ProbeSpecMetricRelabelings:
    def __init__(
        self,
        *,
        action: typing.Optional["ProbeSpecMetricRelabelingsAction"] = None,
        modulus: typing.Optional[jsii.Number] = None,
        regex: typing.Optional[builtins.str] = None,
        replacement: typing.Optional[builtins.str] = None,
        separator: typing.Optional[builtins.str] = None,
        source_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''RelabelConfig allows dynamic rewriting of the label set for targets, alerts, scraped samples and remote write samples.

        More info: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config

        :param action: action to perform based on the regex matching. ``Uppercase`` and ``Lowercase`` actions require Prometheus >= v2.36.0. ``DropEqual`` and ``KeepEqual`` actions require Prometheus >= v2.41.0. Default: "Replace"
        :param modulus: modulus to take of the hash of the source label values. Only applicable when the action is ``HashMod``.
        :param regex: regex defines the regular expression against which the extracted value is matched.
        :param replacement: replacement value against which a Replace action is performed if the regular expression matches. Regex capture groups are available.
        :param separator: separator defines the string between concatenated SourceLabels.
        :param source_labels: sourceLabels defines the source labels select values from existing labels. Their content is concatenated using the configured Separator and matched against the configured regular expression.
        :param target_label: targetLabel defines the label to which the resulting string is written in a replacement. It is mandatory for ``Replace``, ``HashMod``, ``Lowercase``, ``Uppercase``, ``KeepEqual`` and ``DropEqual`` actions. Regex capture groups are available.

        :schema: ProbeSpecMetricRelabelings
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b7df01a5f3a31e8d2329909c14c55b34f6b76669ef783ab0f574f2a4fd436c)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument modulus", value=modulus, expected_type=type_hints["modulus"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument replacement", value=replacement, expected_type=type_hints["replacement"])
            check_type(argname="argument separator", value=separator, expected_type=type_hints["separator"])
            check_type(argname="argument source_labels", value=source_labels, expected_type=type_hints["source_labels"])
            check_type(argname="argument target_label", value=target_label, expected_type=type_hints["target_label"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if modulus is not None:
            self._values["modulus"] = modulus
        if regex is not None:
            self._values["regex"] = regex
        if replacement is not None:
            self._values["replacement"] = replacement
        if separator is not None:
            self._values["separator"] = separator
        if source_labels is not None:
            self._values["source_labels"] = source_labels
        if target_label is not None:
            self._values["target_label"] = target_label

    @builtins.property
    def action(self) -> typing.Optional["ProbeSpecMetricRelabelingsAction"]:
        '''action to perform based on the regex matching.

        ``Uppercase`` and ``Lowercase`` actions require Prometheus >= v2.36.0.
        ``DropEqual`` and ``KeepEqual`` actions require Prometheus >= v2.41.0.

        Default: "Replace"

        :schema: ProbeSpecMetricRelabelings#action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional["ProbeSpecMetricRelabelingsAction"], result)

    @builtins.property
    def modulus(self) -> typing.Optional[jsii.Number]:
        '''modulus to take of the hash of the source label values.

        Only applicable when the action is ``HashMod``.

        :schema: ProbeSpecMetricRelabelings#modulus
        '''
        result = self._values.get("modulus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''regex defines the regular expression against which the extracted value is matched.

        :schema: ProbeSpecMetricRelabelings#regex
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replacement(self) -> typing.Optional[builtins.str]:
        '''replacement value against which a Replace action is performed if the regular expression matches.

        Regex capture groups are available.

        :schema: ProbeSpecMetricRelabelings#replacement
        '''
        result = self._values.get("replacement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def separator(self) -> typing.Optional[builtins.str]:
        '''separator defines the string between concatenated SourceLabels.

        :schema: ProbeSpecMetricRelabelings#separator
        '''
        result = self._values.get("separator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''sourceLabels defines the source labels select values from existing labels.

        Their content is
        concatenated using the configured Separator and matched against the
        configured regular expression.

        :schema: ProbeSpecMetricRelabelings#sourceLabels
        '''
        result = self._values.get("source_labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_label(self) -> typing.Optional[builtins.str]:
        '''targetLabel defines the label to which the resulting string is written in a replacement.

        It is mandatory for ``Replace``, ``HashMod``, ``Lowercase``, ``Uppercase``,
        ``KeepEqual`` and ``DropEqual`` actions.

        Regex capture groups are available.

        :schema: ProbeSpecMetricRelabelings#targetLabel
        '''
        result = self._values.get("target_label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecMetricRelabelings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="comcoreosmonitoring.ProbeSpecMetricRelabelingsAction")
class ProbeSpecMetricRelabelingsAction(enum.Enum):
    '''action to perform based on the regex matching.

    ``Uppercase`` and ``Lowercase`` actions require Prometheus >= v2.36.0.
    ``DropEqual`` and ``KeepEqual`` actions require Prometheus >= v2.41.0.

    Default: "Replace"

    :schema: ProbeSpecMetricRelabelingsAction
    '''

    REPLACE = "REPLACE"
    '''replace.'''
    KEEP = "KEEP"
    '''keep.'''
    DROP = "DROP"
    '''drop.'''
    HASHMOD = "HASHMOD"
    '''hashmod.'''
    LABELMAP = "LABELMAP"
    '''labelmap.'''
    LABELDROP = "LABELDROP"
    '''labeldrop.'''
    LABELKEEP = "LABELKEEP"
    '''labelkeep.'''
    LOWERCASE = "LOWERCASE"
    '''lowercase.'''
    UPPERCASE = "UPPERCASE"
    '''uppercase.'''
    KEEPEQUAL = "KEEPEQUAL"
    '''keepequal.'''
    DROPEQUAL = "DROPEQUAL"
    '''dropequal.'''


class ProbeSpecNativeHistogramMinBucketFactor(
    metaclass=jsii.JSIIMeta,
    jsii_type="comcoreosmonitoring.ProbeSpecNativeHistogramMinBucketFactor",
):
    '''nativeHistogramMinBucketFactor defines if the growth factor of one bucket to the next is smaller than this, buckets will be merged to increase the factor sufficiently.

    It requires Prometheus >= v2.50.0.

    :schema: ProbeSpecNativeHistogramMinBucketFactor
    '''

    @jsii.member(jsii_name="fromNumber")
    @builtins.classmethod
    def from_number(
        cls,
        value: jsii.Number,
    ) -> "ProbeSpecNativeHistogramMinBucketFactor":
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4b130555197feba1c2d7008bc599d472d9b7386f7b29b719e7f32340b972186)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ProbeSpecNativeHistogramMinBucketFactor", jsii.sinvoke(cls, "fromNumber", [value]))

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(
        cls,
        value: builtins.str,
    ) -> "ProbeSpecNativeHistogramMinBucketFactor":
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d8c278e2bddb7a566817def41022cebbb7f0c4e1a3bbb9a2be8e89d44126c54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ProbeSpecNativeHistogramMinBucketFactor", jsii.sinvoke(cls, "fromString", [value]))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Union[builtins.str, jsii.Number]:
        return typing.cast(typing.Union[builtins.str, jsii.Number], jsii.get(self, "value"))


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecOauth2",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "token_url": "tokenUrl",
        "endpoint_params": "endpointParams",
        "no_proxy": "noProxy",
        "proxy_connect_header": "proxyConnectHeader",
        "proxy_from_environment": "proxyFromEnvironment",
        "proxy_url": "proxyUrl",
        "scopes": "scopes",
        "tls_config": "tlsConfig",
    },
)
class ProbeSpecOauth2:
    def __init__(
        self,
        *,
        client_id: typing.Union["ProbeSpecOauth2ClientId", typing.Dict[builtins.str, typing.Any]],
        client_secret: typing.Union["ProbeSpecOauth2ClientSecret", typing.Dict[builtins.str, typing.Any]],
        token_url: builtins.str,
        endpoint_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        no_proxy: typing.Optional[builtins.str] = None,
        proxy_connect_header: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[typing.Union["ProbeSpecOauth2ProxyConnectHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        proxy_from_environment: typing.Optional[builtins.bool] = None,
        proxy_url: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        tls_config: typing.Optional[typing.Union["ProbeSpecOauth2TlsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''oauth2 defines the OAuth2 settings used by the client.

        It requires Prometheus >= 2.27.0.

        Cannot be set at the same time as ``authorization``, ``basicAuth`` or ``bearerTokenSecret``.

        :param client_id: clientId defines a key of a Secret or ConfigMap containing the OAuth2 client's ID.
        :param client_secret: clientSecret defines a key of a Secret containing the OAuth2 client's secret.
        :param token_url: tokenUrl defines the URL to fetch the token from.
        :param endpoint_params: endpointParams configures the HTTP parameters to append to the token URL.
        :param no_proxy: noProxy defines a comma-separated string that can contain IPs, CIDR notation, domain names that should be excluded from proxying. IP and domain names can contain port numbers. It requires Prometheus >= v2.43.0, Alertmanager >= v0.25.0 or Thanos >= v0.32.0.
        :param proxy_connect_header: proxyConnectHeader optionally specifies headers to send to proxies during CONNECT requests. It requires Prometheus >= v2.43.0, Alertmanager >= v0.25.0 or Thanos >= v0.32.0.
        :param proxy_from_environment: proxyFromEnvironment defines whether to use the proxy configuration defined by environment variables (HTTP_PROXY, HTTPS_PROXY, and NO_PROXY). It requires Prometheus >= v2.43.0, Alertmanager >= v0.25.0 or Thanos >= v0.32.0.
        :param proxy_url: proxyUrl defines the HTTP proxy server to use.
        :param scopes: scopes defines the OAuth2 scopes used for the token request.
        :param tls_config: tlsConfig defines the TLS configuration to use when connecting to the OAuth2 server. It requires Prometheus >= v2.43.0.

        :schema: ProbeSpecOauth2
        '''
        if isinstance(client_id, dict):
            client_id = ProbeSpecOauth2ClientId(**client_id)
        if isinstance(client_secret, dict):
            client_secret = ProbeSpecOauth2ClientSecret(**client_secret)
        if isinstance(tls_config, dict):
            tls_config = ProbeSpecOauth2TlsConfig(**tls_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35546638facd27ef81d9c1565abe451319a91571a20f556580e86ba1d20429a2)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument token_url", value=token_url, expected_type=type_hints["token_url"])
            check_type(argname="argument endpoint_params", value=endpoint_params, expected_type=type_hints["endpoint_params"])
            check_type(argname="argument no_proxy", value=no_proxy, expected_type=type_hints["no_proxy"])
            check_type(argname="argument proxy_connect_header", value=proxy_connect_header, expected_type=type_hints["proxy_connect_header"])
            check_type(argname="argument proxy_from_environment", value=proxy_from_environment, expected_type=type_hints["proxy_from_environment"])
            check_type(argname="argument proxy_url", value=proxy_url, expected_type=type_hints["proxy_url"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument tls_config", value=tls_config, expected_type=type_hints["tls_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
            "token_url": token_url,
        }
        if endpoint_params is not None:
            self._values["endpoint_params"] = endpoint_params
        if no_proxy is not None:
            self._values["no_proxy"] = no_proxy
        if proxy_connect_header is not None:
            self._values["proxy_connect_header"] = proxy_connect_header
        if proxy_from_environment is not None:
            self._values["proxy_from_environment"] = proxy_from_environment
        if proxy_url is not None:
            self._values["proxy_url"] = proxy_url
        if scopes is not None:
            self._values["scopes"] = scopes
        if tls_config is not None:
            self._values["tls_config"] = tls_config

    @builtins.property
    def client_id(self) -> "ProbeSpecOauth2ClientId":
        '''clientId defines a key of a Secret or ConfigMap containing the OAuth2 client's ID.

        :schema: ProbeSpecOauth2#clientId
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast("ProbeSpecOauth2ClientId", result)

    @builtins.property
    def client_secret(self) -> "ProbeSpecOauth2ClientSecret":
        '''clientSecret defines a key of a Secret containing the OAuth2 client's secret.

        :schema: ProbeSpecOauth2#clientSecret
        '''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast("ProbeSpecOauth2ClientSecret", result)

    @builtins.property
    def token_url(self) -> builtins.str:
        '''tokenUrl defines the URL to fetch the token from.

        :schema: ProbeSpecOauth2#tokenUrl
        '''
        result = self._values.get("token_url")
        assert result is not None, "Required property 'token_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''endpointParams configures the HTTP parameters to append to the token URL.

        :schema: ProbeSpecOauth2#endpointParams
        '''
        result = self._values.get("endpoint_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def no_proxy(self) -> typing.Optional[builtins.str]:
        '''noProxy defines a comma-separated string that can contain IPs, CIDR notation, domain names that should be excluded from proxying.

        IP and domain names can
        contain port numbers.

        It requires Prometheus >= v2.43.0, Alertmanager >= v0.25.0 or Thanos >= v0.32.0.

        :schema: ProbeSpecOauth2#noProxy
        '''
        result = self._values.get("no_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_connect_header(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List["ProbeSpecOauth2ProxyConnectHeader"]]]:
        '''proxyConnectHeader optionally specifies headers to send to proxies during CONNECT requests.

        It requires Prometheus >= v2.43.0, Alertmanager >= v0.25.0 or Thanos >= v0.32.0.

        :schema: ProbeSpecOauth2#proxyConnectHeader
        '''
        result = self._values.get("proxy_connect_header")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List["ProbeSpecOauth2ProxyConnectHeader"]]], result)

    @builtins.property
    def proxy_from_environment(self) -> typing.Optional[builtins.bool]:
        '''proxyFromEnvironment defines whether to use the proxy configuration defined by environment variables (HTTP_PROXY, HTTPS_PROXY, and NO_PROXY).

        It requires Prometheus >= v2.43.0, Alertmanager >= v0.25.0 or Thanos >= v0.32.0.

        :schema: ProbeSpecOauth2#proxyFromEnvironment
        '''
        result = self._values.get("proxy_from_environment")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def proxy_url(self) -> typing.Optional[builtins.str]:
        '''proxyUrl defines the HTTP proxy server to use.

        :schema: ProbeSpecOauth2#proxyUrl
        '''
        result = self._values.get("proxy_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''scopes defines the OAuth2 scopes used for the token request.

        :schema: ProbeSpecOauth2#scopes
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tls_config(self) -> typing.Optional["ProbeSpecOauth2TlsConfig"]:
        '''tlsConfig defines the TLS configuration to use when connecting to the OAuth2 server.

        It requires Prometheus >= v2.43.0.

        :schema: ProbeSpecOauth2#tlsConfig
        '''
        result = self._values.get("tls_config")
        return typing.cast(typing.Optional["ProbeSpecOauth2TlsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecOauth2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecOauth2ClientId",
    jsii_struct_bases=[],
    name_mapping={"config_map": "configMap", "secret": "secret"},
)
class ProbeSpecOauth2ClientId:
    def __init__(
        self,
        *,
        config_map: typing.Optional[typing.Union["ProbeSpecOauth2ClientIdConfigMap", typing.Dict[builtins.str, typing.Any]]] = None,
        secret: typing.Optional[typing.Union["ProbeSpecOauth2ClientIdSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''clientId defines a key of a Secret or ConfigMap containing the OAuth2 client's ID.

        :param config_map: configMap defines the ConfigMap containing data to use for the targets.
        :param secret: secret defines the Secret containing data to use for the targets.

        :schema: ProbeSpecOauth2ClientId
        '''
        if isinstance(config_map, dict):
            config_map = ProbeSpecOauth2ClientIdConfigMap(**config_map)
        if isinstance(secret, dict):
            secret = ProbeSpecOauth2ClientIdSecret(**secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be1be640787caefbccf5bf6ea2c41346de4deaa3542fa016ffcd1ad2f7b03947)
            check_type(argname="argument config_map", value=config_map, expected_type=type_hints["config_map"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config_map is not None:
            self._values["config_map"] = config_map
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def config_map(self) -> typing.Optional["ProbeSpecOauth2ClientIdConfigMap"]:
        '''configMap defines the ConfigMap containing data to use for the targets.

        :schema: ProbeSpecOauth2ClientId#configMap
        '''
        result = self._values.get("config_map")
        return typing.cast(typing.Optional["ProbeSpecOauth2ClientIdConfigMap"], result)

    @builtins.property
    def secret(self) -> typing.Optional["ProbeSpecOauth2ClientIdSecret"]:
        '''secret defines the Secret containing data to use for the targets.

        :schema: ProbeSpecOauth2ClientId#secret
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional["ProbeSpecOauth2ClientIdSecret"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecOauth2ClientId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecOauth2ClientIdConfigMap",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecOauth2ClientIdConfigMap:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''configMap defines the ConfigMap containing data to use for the targets.

        :param key: The key to select.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the ConfigMap or its key must be defined.

        :schema: ProbeSpecOauth2ClientIdConfigMap
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b58566d2cc8954a47735bf7be6b762a394014c89472a4e9a617944a055f9eba)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key to select.

        :schema: ProbeSpecOauth2ClientIdConfigMap#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecOauth2ClientIdConfigMap#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the ConfigMap or its key must be defined.

        :schema: ProbeSpecOauth2ClientIdConfigMap#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecOauth2ClientIdConfigMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecOauth2ClientIdSecret",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecOauth2ClientIdSecret:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''secret defines the Secret containing data to use for the targets.

        :param key: The key of the secret to select from. Must be a valid secret key.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecOauth2ClientIdSecret
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3883f2226aad7334fc8c12f1bd7a408a3265db413dbe8a1e3d4a338d6977eb5)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the secret to select from.

        Must be a valid secret key.

        :schema: ProbeSpecOauth2ClientIdSecret#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecOauth2ClientIdSecret#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecOauth2ClientIdSecret#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecOauth2ClientIdSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecOauth2ClientSecret",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecOauth2ClientSecret:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''clientSecret defines a key of a Secret containing the OAuth2 client's secret.

        :param key: The key of the secret to select from. Must be a valid secret key.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecOauth2ClientSecret
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc4814e43f5970f5d96976d6e9d6055b8a3423197f1bd40f0b4cc46f6dec7d51)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the secret to select from.

        Must be a valid secret key.

        :schema: ProbeSpecOauth2ClientSecret#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecOauth2ClientSecret#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecOauth2ClientSecret#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecOauth2ClientSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecOauth2ProxyConnectHeader",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecOauth2ProxyConnectHeader:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''SecretKeySelector selects a key of a Secret.

        :param key: The key of the secret to select from. Must be a valid secret key.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecOauth2ProxyConnectHeader
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15168185ff890e76ebda9406137eb68adc01cdc9c5aab9c30a2c5826a7006e00)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the secret to select from.

        Must be a valid secret key.

        :schema: ProbeSpecOauth2ProxyConnectHeader#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecOauth2ProxyConnectHeader#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecOauth2ProxyConnectHeader#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecOauth2ProxyConnectHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecOauth2TlsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "ca": "ca",
        "cert": "cert",
        "insecure_skip_verify": "insecureSkipVerify",
        "key_secret": "keySecret",
        "max_version": "maxVersion",
        "min_version": "minVersion",
        "server_name": "serverName",
    },
)
class ProbeSpecOauth2TlsConfig:
    def __init__(
        self,
        *,
        ca: typing.Optional[typing.Union["ProbeSpecOauth2TlsConfigCa", typing.Dict[builtins.str, typing.Any]]] = None,
        cert: typing.Optional[typing.Union["ProbeSpecOauth2TlsConfigCert", typing.Dict[builtins.str, typing.Any]]] = None,
        insecure_skip_verify: typing.Optional[builtins.bool] = None,
        key_secret: typing.Optional[typing.Union["ProbeSpecOauth2TlsConfigKeySecret", typing.Dict[builtins.str, typing.Any]]] = None,
        max_version: typing.Optional["ProbeSpecOauth2TlsConfigMaxVersion"] = None,
        min_version: typing.Optional["ProbeSpecOauth2TlsConfigMinVersion"] = None,
        server_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''tlsConfig defines the TLS configuration to use when connecting to the OAuth2 server.

        It requires Prometheus >= v2.43.0.

        :param ca: ca defines the Certificate authority used when verifying server certificates.
        :param cert: cert defines the Client certificate to present when doing client-authentication.
        :param insecure_skip_verify: insecureSkipVerify defines how to disable target certificate validation.
        :param key_secret: keySecret defines the Secret containing the client key file for the targets.
        :param max_version: maxVersion defines the maximum acceptable TLS version. It requires Prometheus >= v2.41.0 or Thanos >= v0.31.0.
        :param min_version: minVersion defines the minimum acceptable TLS version. It requires Prometheus >= v2.35.0 or Thanos >= v0.28.0.
        :param server_name: serverName is used to verify the hostname for the targets.

        :schema: ProbeSpecOauth2TlsConfig
        '''
        if isinstance(ca, dict):
            ca = ProbeSpecOauth2TlsConfigCa(**ca)
        if isinstance(cert, dict):
            cert = ProbeSpecOauth2TlsConfigCert(**cert)
        if isinstance(key_secret, dict):
            key_secret = ProbeSpecOauth2TlsConfigKeySecret(**key_secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acab03ee682702fd6d01e755686c70644b8c90eb20338257444d40971a8fa5e5)
            check_type(argname="argument ca", value=ca, expected_type=type_hints["ca"])
            check_type(argname="argument cert", value=cert, expected_type=type_hints["cert"])
            check_type(argname="argument insecure_skip_verify", value=insecure_skip_verify, expected_type=type_hints["insecure_skip_verify"])
            check_type(argname="argument key_secret", value=key_secret, expected_type=type_hints["key_secret"])
            check_type(argname="argument max_version", value=max_version, expected_type=type_hints["max_version"])
            check_type(argname="argument min_version", value=min_version, expected_type=type_hints["min_version"])
            check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ca is not None:
            self._values["ca"] = ca
        if cert is not None:
            self._values["cert"] = cert
        if insecure_skip_verify is not None:
            self._values["insecure_skip_verify"] = insecure_skip_verify
        if key_secret is not None:
            self._values["key_secret"] = key_secret
        if max_version is not None:
            self._values["max_version"] = max_version
        if min_version is not None:
            self._values["min_version"] = min_version
        if server_name is not None:
            self._values["server_name"] = server_name

    @builtins.property
    def ca(self) -> typing.Optional["ProbeSpecOauth2TlsConfigCa"]:
        '''ca defines the Certificate authority used when verifying server certificates.

        :schema: ProbeSpecOauth2TlsConfig#ca
        '''
        result = self._values.get("ca")
        return typing.cast(typing.Optional["ProbeSpecOauth2TlsConfigCa"], result)

    @builtins.property
    def cert(self) -> typing.Optional["ProbeSpecOauth2TlsConfigCert"]:
        '''cert defines the Client certificate to present when doing client-authentication.

        :schema: ProbeSpecOauth2TlsConfig#cert
        '''
        result = self._values.get("cert")
        return typing.cast(typing.Optional["ProbeSpecOauth2TlsConfigCert"], result)

    @builtins.property
    def insecure_skip_verify(self) -> typing.Optional[builtins.bool]:
        '''insecureSkipVerify defines how to disable target certificate validation.

        :schema: ProbeSpecOauth2TlsConfig#insecureSkipVerify
        '''
        result = self._values.get("insecure_skip_verify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key_secret(self) -> typing.Optional["ProbeSpecOauth2TlsConfigKeySecret"]:
        '''keySecret defines the Secret containing the client key file for the targets.

        :schema: ProbeSpecOauth2TlsConfig#keySecret
        '''
        result = self._values.get("key_secret")
        return typing.cast(typing.Optional["ProbeSpecOauth2TlsConfigKeySecret"], result)

    @builtins.property
    def max_version(self) -> typing.Optional["ProbeSpecOauth2TlsConfigMaxVersion"]:
        '''maxVersion defines the maximum acceptable TLS version.

        It requires Prometheus >= v2.41.0 or Thanos >= v0.31.0.

        :schema: ProbeSpecOauth2TlsConfig#maxVersion
        '''
        result = self._values.get("max_version")
        return typing.cast(typing.Optional["ProbeSpecOauth2TlsConfigMaxVersion"], result)

    @builtins.property
    def min_version(self) -> typing.Optional["ProbeSpecOauth2TlsConfigMinVersion"]:
        '''minVersion defines the minimum acceptable TLS version.

        It requires Prometheus >= v2.35.0 or Thanos >= v0.28.0.

        :schema: ProbeSpecOauth2TlsConfig#minVersion
        '''
        result = self._values.get("min_version")
        return typing.cast(typing.Optional["ProbeSpecOauth2TlsConfigMinVersion"], result)

    @builtins.property
    def server_name(self) -> typing.Optional[builtins.str]:
        '''serverName is used to verify the hostname for the targets.

        :schema: ProbeSpecOauth2TlsConfig#serverName
        '''
        result = self._values.get("server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecOauth2TlsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecOauth2TlsConfigCa",
    jsii_struct_bases=[],
    name_mapping={"config_map": "configMap", "secret": "secret"},
)
class ProbeSpecOauth2TlsConfigCa:
    def __init__(
        self,
        *,
        config_map: typing.Optional[typing.Union["ProbeSpecOauth2TlsConfigCaConfigMap", typing.Dict[builtins.str, typing.Any]]] = None,
        secret: typing.Optional[typing.Union["ProbeSpecOauth2TlsConfigCaSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''ca defines the Certificate authority used when verifying server certificates.

        :param config_map: configMap defines the ConfigMap containing data to use for the targets.
        :param secret: secret defines the Secret containing data to use for the targets.

        :schema: ProbeSpecOauth2TlsConfigCa
        '''
        if isinstance(config_map, dict):
            config_map = ProbeSpecOauth2TlsConfigCaConfigMap(**config_map)
        if isinstance(secret, dict):
            secret = ProbeSpecOauth2TlsConfigCaSecret(**secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b9fbb23975748c32531df12669a8d0336e3f150fe8dfc6d0523b7872181e9db)
            check_type(argname="argument config_map", value=config_map, expected_type=type_hints["config_map"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config_map is not None:
            self._values["config_map"] = config_map
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def config_map(self) -> typing.Optional["ProbeSpecOauth2TlsConfigCaConfigMap"]:
        '''configMap defines the ConfigMap containing data to use for the targets.

        :schema: ProbeSpecOauth2TlsConfigCa#configMap
        '''
        result = self._values.get("config_map")
        return typing.cast(typing.Optional["ProbeSpecOauth2TlsConfigCaConfigMap"], result)

    @builtins.property
    def secret(self) -> typing.Optional["ProbeSpecOauth2TlsConfigCaSecret"]:
        '''secret defines the Secret containing data to use for the targets.

        :schema: ProbeSpecOauth2TlsConfigCa#secret
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional["ProbeSpecOauth2TlsConfigCaSecret"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecOauth2TlsConfigCa(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecOauth2TlsConfigCaConfigMap",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecOauth2TlsConfigCaConfigMap:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''configMap defines the ConfigMap containing data to use for the targets.

        :param key: The key to select.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the ConfigMap or its key must be defined.

        :schema: ProbeSpecOauth2TlsConfigCaConfigMap
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb44bff72110d97ac3438464c8c567658490b004d26407730c443ccc51b13493)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key to select.

        :schema: ProbeSpecOauth2TlsConfigCaConfigMap#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecOauth2TlsConfigCaConfigMap#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the ConfigMap or its key must be defined.

        :schema: ProbeSpecOauth2TlsConfigCaConfigMap#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecOauth2TlsConfigCaConfigMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecOauth2TlsConfigCaSecret",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecOauth2TlsConfigCaSecret:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''secret defines the Secret containing data to use for the targets.

        :param key: The key of the secret to select from. Must be a valid secret key.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecOauth2TlsConfigCaSecret
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ebb235751ba9f0be493e52ef41f277eeec2f4f835eee9624496ef01c19958b5)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the secret to select from.

        Must be a valid secret key.

        :schema: ProbeSpecOauth2TlsConfigCaSecret#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecOauth2TlsConfigCaSecret#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecOauth2TlsConfigCaSecret#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecOauth2TlsConfigCaSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecOauth2TlsConfigCert",
    jsii_struct_bases=[],
    name_mapping={"config_map": "configMap", "secret": "secret"},
)
class ProbeSpecOauth2TlsConfigCert:
    def __init__(
        self,
        *,
        config_map: typing.Optional[typing.Union["ProbeSpecOauth2TlsConfigCertConfigMap", typing.Dict[builtins.str, typing.Any]]] = None,
        secret: typing.Optional[typing.Union["ProbeSpecOauth2TlsConfigCertSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''cert defines the Client certificate to present when doing client-authentication.

        :param config_map: configMap defines the ConfigMap containing data to use for the targets.
        :param secret: secret defines the Secret containing data to use for the targets.

        :schema: ProbeSpecOauth2TlsConfigCert
        '''
        if isinstance(config_map, dict):
            config_map = ProbeSpecOauth2TlsConfigCertConfigMap(**config_map)
        if isinstance(secret, dict):
            secret = ProbeSpecOauth2TlsConfigCertSecret(**secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa77d74aa81f6f522990bdc835c51cbbacfbaaf72af7fa1e3fc03fca7a149e0d)
            check_type(argname="argument config_map", value=config_map, expected_type=type_hints["config_map"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config_map is not None:
            self._values["config_map"] = config_map
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def config_map(self) -> typing.Optional["ProbeSpecOauth2TlsConfigCertConfigMap"]:
        '''configMap defines the ConfigMap containing data to use for the targets.

        :schema: ProbeSpecOauth2TlsConfigCert#configMap
        '''
        result = self._values.get("config_map")
        return typing.cast(typing.Optional["ProbeSpecOauth2TlsConfigCertConfigMap"], result)

    @builtins.property
    def secret(self) -> typing.Optional["ProbeSpecOauth2TlsConfigCertSecret"]:
        '''secret defines the Secret containing data to use for the targets.

        :schema: ProbeSpecOauth2TlsConfigCert#secret
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional["ProbeSpecOauth2TlsConfigCertSecret"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecOauth2TlsConfigCert(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecOauth2TlsConfigCertConfigMap",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecOauth2TlsConfigCertConfigMap:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''configMap defines the ConfigMap containing data to use for the targets.

        :param key: The key to select.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the ConfigMap or its key must be defined.

        :schema: ProbeSpecOauth2TlsConfigCertConfigMap
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf145604647ba536a0b9fb2de88a38dc6edc7f9a5b0f218814bad74a25fedf7)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key to select.

        :schema: ProbeSpecOauth2TlsConfigCertConfigMap#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecOauth2TlsConfigCertConfigMap#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the ConfigMap or its key must be defined.

        :schema: ProbeSpecOauth2TlsConfigCertConfigMap#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecOauth2TlsConfigCertConfigMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecOauth2TlsConfigCertSecret",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecOauth2TlsConfigCertSecret:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''secret defines the Secret containing data to use for the targets.

        :param key: The key of the secret to select from. Must be a valid secret key.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecOauth2TlsConfigCertSecret
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1ee302452088816f5aa0ff7b10ed5e5fb4982d155b44ac8bbf2bf6b86f4790)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the secret to select from.

        Must be a valid secret key.

        :schema: ProbeSpecOauth2TlsConfigCertSecret#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecOauth2TlsConfigCertSecret#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecOauth2TlsConfigCertSecret#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecOauth2TlsConfigCertSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecOauth2TlsConfigKeySecret",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecOauth2TlsConfigKeySecret:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''keySecret defines the Secret containing the client key file for the targets.

        :param key: The key of the secret to select from. Must be a valid secret key.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecOauth2TlsConfigKeySecret
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33dc52b7c1489b1ef2cb0651104939ff50b5f5fc1d5e6875fce37f06ffe66295)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the secret to select from.

        Must be a valid secret key.

        :schema: ProbeSpecOauth2TlsConfigKeySecret#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecOauth2TlsConfigKeySecret#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecOauth2TlsConfigKeySecret#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecOauth2TlsConfigKeySecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="comcoreosmonitoring.ProbeSpecOauth2TlsConfigMaxVersion")
class ProbeSpecOauth2TlsConfigMaxVersion(enum.Enum):
    '''maxVersion defines the maximum acceptable TLS version.

    It requires Prometheus >= v2.41.0 or Thanos >= v0.31.0.

    :schema: ProbeSpecOauth2TlsConfigMaxVersion
    '''

    TLS10 = "TLS10"
    '''TLS10.'''
    TLS11 = "TLS11"
    '''TLS11.'''
    TLS12 = "TLS12"
    '''TLS12.'''
    TLS13 = "TLS13"
    '''TLS13.'''


@jsii.enum(jsii_type="comcoreosmonitoring.ProbeSpecOauth2TlsConfigMinVersion")
class ProbeSpecOauth2TlsConfigMinVersion(enum.Enum):
    '''minVersion defines the minimum acceptable TLS version.

    It requires Prometheus >= v2.35.0 or Thanos >= v0.28.0.

    :schema: ProbeSpecOauth2TlsConfigMinVersion
    '''

    TLS10 = "TLS10"
    '''TLS10.'''
    TLS11 = "TLS11"
    '''TLS11.'''
    TLS12 = "TLS12"
    '''TLS12.'''
    TLS13 = "TLS13"
    '''TLS13.'''


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecParams",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class ProbeSpecParams:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''ProbeParam defines specification of extra parameters for a Probe.

        :param name: name defines the parameter name.
        :param values: values defines the parameter values.

        :schema: ProbeSpecParams
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f83e6f1b9e7885581ddfaea5d163a9a2c94860c9d3f775f17b2f2191928513d2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def name(self) -> builtins.str:
        '''name defines the parameter name.

        :schema: ProbeSpecParams#name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''values defines the parameter values.

        :schema: ProbeSpecParams#values
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecProber",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "no_proxy": "noProxy",
        "path": "path",
        "proxy_connect_header": "proxyConnectHeader",
        "proxy_from_environment": "proxyFromEnvironment",
        "proxy_url": "proxyUrl",
        "scheme": "scheme",
    },
)
class ProbeSpecProber:
    def __init__(
        self,
        *,
        url: builtins.str,
        no_proxy: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        proxy_connect_header: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[typing.Union["ProbeSpecProberProxyConnectHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        proxy_from_environment: typing.Optional[builtins.bool] = None,
        proxy_url: typing.Optional[builtins.str] = None,
        scheme: typing.Optional["ProbeSpecProberScheme"] = None,
    ) -> None:
        '''prober defines the specification for the prober to use for probing targets.

        The prober.URL parameter is required. Targets cannot be probed if left empty.

        :param url: url defines the address of the prober. Unlike what the name indicates, the value should be in the form of ``address:port`` without any scheme which should be specified in the ``scheme`` field.
        :param no_proxy: noProxy defines a comma-separated string that can contain IPs, CIDR notation, domain names that should be excluded from proxying. IP and domain names can contain port numbers. It requires Prometheus >= v2.43.0, Alertmanager >= v0.25.0 or Thanos >= v0.32.0.
        :param path: path to collect metrics from. Defaults to ``/probe``. Default: probe`.
        :param proxy_connect_header: proxyConnectHeader optionally specifies headers to send to proxies during CONNECT requests. It requires Prometheus >= v2.43.0, Alertmanager >= v0.25.0 or Thanos >= v0.32.0.
        :param proxy_from_environment: proxyFromEnvironment defines whether to use the proxy configuration defined by environment variables (HTTP_PROXY, HTTPS_PROXY, and NO_PROXY). It requires Prometheus >= v2.43.0, Alertmanager >= v0.25.0 or Thanos >= v0.32.0.
        :param proxy_url: proxyUrl defines the HTTP proxy server to use.
        :param scheme: scheme defines the HTTP scheme to use when scraping the prober.

        :schema: ProbeSpecProber
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6684cb5ff968185a87d2fade885ee91d9329d7babe8bc8fbb69c24e63cd7cdb7)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument no_proxy", value=no_proxy, expected_type=type_hints["no_proxy"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument proxy_connect_header", value=proxy_connect_header, expected_type=type_hints["proxy_connect_header"])
            check_type(argname="argument proxy_from_environment", value=proxy_from_environment, expected_type=type_hints["proxy_from_environment"])
            check_type(argname="argument proxy_url", value=proxy_url, expected_type=type_hints["proxy_url"])
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if no_proxy is not None:
            self._values["no_proxy"] = no_proxy
        if path is not None:
            self._values["path"] = path
        if proxy_connect_header is not None:
            self._values["proxy_connect_header"] = proxy_connect_header
        if proxy_from_environment is not None:
            self._values["proxy_from_environment"] = proxy_from_environment
        if proxy_url is not None:
            self._values["proxy_url"] = proxy_url
        if scheme is not None:
            self._values["scheme"] = scheme

    @builtins.property
    def url(self) -> builtins.str:
        '''url defines the address of the prober.

        Unlike what the name indicates, the value should be in the form of
        ``address:port`` without any scheme which should be specified in the
        ``scheme`` field.

        :schema: ProbeSpecProber#url
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def no_proxy(self) -> typing.Optional[builtins.str]:
        '''noProxy defines a comma-separated string that can contain IPs, CIDR notation, domain names that should be excluded from proxying.

        IP and domain names can
        contain port numbers.

        It requires Prometheus >= v2.43.0, Alertmanager >= v0.25.0 or Thanos >= v0.32.0.

        :schema: ProbeSpecProber#noProxy
        '''
        result = self._values.get("no_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''path to collect metrics from.

        Defaults to ``/probe``.

        :default: probe`.

        :schema: ProbeSpecProber#path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_connect_header(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List["ProbeSpecProberProxyConnectHeader"]]]:
        '''proxyConnectHeader optionally specifies headers to send to proxies during CONNECT requests.

        It requires Prometheus >= v2.43.0, Alertmanager >= v0.25.0 or Thanos >= v0.32.0.

        :schema: ProbeSpecProber#proxyConnectHeader
        '''
        result = self._values.get("proxy_connect_header")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List["ProbeSpecProberProxyConnectHeader"]]], result)

    @builtins.property
    def proxy_from_environment(self) -> typing.Optional[builtins.bool]:
        '''proxyFromEnvironment defines whether to use the proxy configuration defined by environment variables (HTTP_PROXY, HTTPS_PROXY, and NO_PROXY).

        It requires Prometheus >= v2.43.0, Alertmanager >= v0.25.0 or Thanos >= v0.32.0.

        :schema: ProbeSpecProber#proxyFromEnvironment
        '''
        result = self._values.get("proxy_from_environment")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def proxy_url(self) -> typing.Optional[builtins.str]:
        '''proxyUrl defines the HTTP proxy server to use.

        :schema: ProbeSpecProber#proxyUrl
        '''
        result = self._values.get("proxy_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheme(self) -> typing.Optional["ProbeSpecProberScheme"]:
        '''scheme defines the HTTP scheme to use when scraping the prober.

        :schema: ProbeSpecProber#scheme
        '''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional["ProbeSpecProberScheme"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecProber(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecProberProxyConnectHeader",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecProberProxyConnectHeader:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''SecretKeySelector selects a key of a Secret.

        :param key: The key of the secret to select from. Must be a valid secret key.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecProberProxyConnectHeader
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__735075c33de8beaf61a817a03a8a9ef456504a89e716a6b517da4fee912fe297)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the secret to select from.

        Must be a valid secret key.

        :schema: ProbeSpecProberProxyConnectHeader#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecProberProxyConnectHeader#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecProberProxyConnectHeader#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecProberProxyConnectHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="comcoreosmonitoring.ProbeSpecProberScheme")
class ProbeSpecProberScheme(enum.Enum):
    '''scheme defines the HTTP scheme to use when scraping the prober.

    :schema: ProbeSpecProberScheme
    '''

    HTTP = "HTTP"
    '''http.'''
    HTTPS = "HTTPS"
    '''https.'''


@jsii.enum(jsii_type="comcoreosmonitoring.ProbeSpecScrapeProtocols")
class ProbeSpecScrapeProtocols(enum.Enum):
    '''ScrapeProtocol represents a protocol used by Prometheus for scraping metrics.

    Supported values are:

    - ``OpenMetricsText0.0.1``
    - ``OpenMetricsText1.0.0``
    - ``PrometheusProto``
    - ``PrometheusText0.0.4``
    - ``PrometheusText1.0.0``

    :schema: ProbeSpecScrapeProtocols
    '''

    PROMETHEUS_PROTO = "PROMETHEUS_PROTO"
    '''PrometheusProto.'''
    OPEN_METRICS_TEXT0_0_1 = "OPEN_METRICS_TEXT0_0_1"
    '''OpenMetricsText0.0.1.'''
    OPEN_METRICS_TEXT1_0_0 = "OPEN_METRICS_TEXT1_0_0"
    '''OpenMetricsText1.0.0.'''
    PROMETHEUS_TEXT0_0_4 = "PROMETHEUS_TEXT0_0_4"
    '''PrometheusText0.0.4.'''
    PROMETHEUS_TEXT1_0_0 = "PROMETHEUS_TEXT1_0_0"
    '''PrometheusText1.0.0.'''


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecTargets",
    jsii_struct_bases=[],
    name_mapping={"ingress": "ingress", "static_config": "staticConfig"},
)
class ProbeSpecTargets:
    def __init__(
        self,
        *,
        ingress: typing.Optional[typing.Union["ProbeSpecTargetsIngress", typing.Dict[builtins.str, typing.Any]]] = None,
        static_config: typing.Optional[typing.Union["ProbeSpecTargetsStaticConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''targets defines a set of static or dynamically discovered targets to probe.

        :param ingress: ingress defines the Ingress objects to probe and the relabeling configuration. If ``staticConfig`` is also defined, ``staticConfig`` takes precedence.
        :param static_config: staticConfig defines the static list of targets to probe and the relabeling configuration. If ``ingress`` is also defined, ``staticConfig`` takes precedence. More info: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#static_config.

        :schema: ProbeSpecTargets
        '''
        if isinstance(ingress, dict):
            ingress = ProbeSpecTargetsIngress(**ingress)
        if isinstance(static_config, dict):
            static_config = ProbeSpecTargetsStaticConfig(**static_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb3c2540b1ee2c4ddde6e123dcd197b358060a8869e20cd6c41672ed67f10a20)
            check_type(argname="argument ingress", value=ingress, expected_type=type_hints["ingress"])
            check_type(argname="argument static_config", value=static_config, expected_type=type_hints["static_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ingress is not None:
            self._values["ingress"] = ingress
        if static_config is not None:
            self._values["static_config"] = static_config

    @builtins.property
    def ingress(self) -> typing.Optional["ProbeSpecTargetsIngress"]:
        '''ingress defines the Ingress objects to probe and the relabeling configuration.

        If ``staticConfig`` is also defined, ``staticConfig`` takes precedence.

        :schema: ProbeSpecTargets#ingress
        '''
        result = self._values.get("ingress")
        return typing.cast(typing.Optional["ProbeSpecTargetsIngress"], result)

    @builtins.property
    def static_config(self) -> typing.Optional["ProbeSpecTargetsStaticConfig"]:
        '''staticConfig defines the static list of targets to probe and the relabeling configuration.

        If ``ingress`` is also defined, ``staticConfig`` takes precedence.
        More info: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#static_config.

        :schema: ProbeSpecTargets#staticConfig
        '''
        result = self._values.get("static_config")
        return typing.cast(typing.Optional["ProbeSpecTargetsStaticConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecTargetsIngress",
    jsii_struct_bases=[],
    name_mapping={
        "namespace_selector": "namespaceSelector",
        "relabeling_configs": "relabelingConfigs",
        "selector": "selector",
    },
)
class ProbeSpecTargetsIngress:
    def __init__(
        self,
        *,
        namespace_selector: typing.Optional[typing.Union["ProbeSpecTargetsIngressNamespaceSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        relabeling_configs: typing.Optional[typing.Sequence[typing.Union["ProbeSpecTargetsIngressRelabelingConfigs", typing.Dict[builtins.str, typing.Any]]]] = None,
        selector: typing.Optional[typing.Union["ProbeSpecTargetsIngressSelector", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''ingress defines the Ingress objects to probe and the relabeling configuration.

        If ``staticConfig`` is also defined, ``staticConfig`` takes precedence.

        :param namespace_selector: namespaceSelector defines from which namespaces to select Ingress objects.
        :param relabeling_configs: relabelingConfigs to apply to the label set of the target before it gets scraped. The original ingress address is available via the ``__tmp_prometheus_ingress_address`` label. It can be used to customize the probed URL. The original scrape job's name is available via the ``__tmp_prometheus_job_name`` label. More info: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config
        :param selector: selector to select the Ingress objects.

        :schema: ProbeSpecTargetsIngress
        '''
        if isinstance(namespace_selector, dict):
            namespace_selector = ProbeSpecTargetsIngressNamespaceSelector(**namespace_selector)
        if isinstance(selector, dict):
            selector = ProbeSpecTargetsIngressSelector(**selector)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__557d9655fcc58a0dbbcd62cd19e97562f13c2ffcfe419b3f3753a95f63268155)
            check_type(argname="argument namespace_selector", value=namespace_selector, expected_type=type_hints["namespace_selector"])
            check_type(argname="argument relabeling_configs", value=relabeling_configs, expected_type=type_hints["relabeling_configs"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if namespace_selector is not None:
            self._values["namespace_selector"] = namespace_selector
        if relabeling_configs is not None:
            self._values["relabeling_configs"] = relabeling_configs
        if selector is not None:
            self._values["selector"] = selector

    @builtins.property
    def namespace_selector(
        self,
    ) -> typing.Optional["ProbeSpecTargetsIngressNamespaceSelector"]:
        '''namespaceSelector defines from which namespaces to select Ingress objects.

        :schema: ProbeSpecTargetsIngress#namespaceSelector
        '''
        result = self._values.get("namespace_selector")
        return typing.cast(typing.Optional["ProbeSpecTargetsIngressNamespaceSelector"], result)

    @builtins.property
    def relabeling_configs(
        self,
    ) -> typing.Optional[typing.List["ProbeSpecTargetsIngressRelabelingConfigs"]]:
        '''relabelingConfigs to apply to the label set of the target before it gets scraped.

        The original ingress address is available via the
        ``__tmp_prometheus_ingress_address`` label. It can be used to customize the
        probed URL.
        The original scrape job's name is available via the ``__tmp_prometheus_job_name`` label.
        More info: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config

        :schema: ProbeSpecTargetsIngress#relabelingConfigs
        '''
        result = self._values.get("relabeling_configs")
        return typing.cast(typing.Optional[typing.List["ProbeSpecTargetsIngressRelabelingConfigs"]], result)

    @builtins.property
    def selector(self) -> typing.Optional["ProbeSpecTargetsIngressSelector"]:
        '''selector to select the Ingress objects.

        :schema: ProbeSpecTargetsIngress#selector
        '''
        result = self._values.get("selector")
        return typing.cast(typing.Optional["ProbeSpecTargetsIngressSelector"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecTargetsIngress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecTargetsIngressNamespaceSelector",
    jsii_struct_bases=[],
    name_mapping={"any": "any", "match_names": "matchNames"},
)
class ProbeSpecTargetsIngressNamespaceSelector:
    def __init__(
        self,
        *,
        any: typing.Optional[builtins.bool] = None,
        match_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''namespaceSelector defines from which namespaces to select Ingress objects.

        :param any: any defines the boolean describing whether all namespaces are selected in contrast to a list restricting them.
        :param match_names: matchNames defines the list of namespace names to select from.

        :schema: ProbeSpecTargetsIngressNamespaceSelector
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ddf059c2fe1e2ea0fa1c287113225d84e1ecfb842e8fc2e3de29f020d957f78)
            check_type(argname="argument any", value=any, expected_type=type_hints["any"])
            check_type(argname="argument match_names", value=match_names, expected_type=type_hints["match_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if any is not None:
            self._values["any"] = any
        if match_names is not None:
            self._values["match_names"] = match_names

    @builtins.property
    def any(self) -> typing.Optional[builtins.bool]:
        '''any defines the boolean describing whether all namespaces are selected in contrast to a list restricting them.

        :schema: ProbeSpecTargetsIngressNamespaceSelector#any
        '''
        result = self._values.get("any")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def match_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''matchNames defines the list of namespace names to select from.

        :schema: ProbeSpecTargetsIngressNamespaceSelector#matchNames
        '''
        result = self._values.get("match_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecTargetsIngressNamespaceSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecTargetsIngressRelabelingConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "modulus": "modulus",
        "regex": "regex",
        "replacement": "replacement",
        "separator": "separator",
        "source_labels": "sourceLabels",
        "target_label": "targetLabel",
    },
)
class ProbeSpecTargetsIngressRelabelingConfigs:
    def __init__(
        self,
        *,
        action: typing.Optional["ProbeSpecTargetsIngressRelabelingConfigsAction"] = None,
        modulus: typing.Optional[jsii.Number] = None,
        regex: typing.Optional[builtins.str] = None,
        replacement: typing.Optional[builtins.str] = None,
        separator: typing.Optional[builtins.str] = None,
        source_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''RelabelConfig allows dynamic rewriting of the label set for targets, alerts, scraped samples and remote write samples.

        More info: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config

        :param action: action to perform based on the regex matching. ``Uppercase`` and ``Lowercase`` actions require Prometheus >= v2.36.0. ``DropEqual`` and ``KeepEqual`` actions require Prometheus >= v2.41.0. Default: "Replace"
        :param modulus: modulus to take of the hash of the source label values. Only applicable when the action is ``HashMod``.
        :param regex: regex defines the regular expression against which the extracted value is matched.
        :param replacement: replacement value against which a Replace action is performed if the regular expression matches. Regex capture groups are available.
        :param separator: separator defines the string between concatenated SourceLabels.
        :param source_labels: sourceLabels defines the source labels select values from existing labels. Their content is concatenated using the configured Separator and matched against the configured regular expression.
        :param target_label: targetLabel defines the label to which the resulting string is written in a replacement. It is mandatory for ``Replace``, ``HashMod``, ``Lowercase``, ``Uppercase``, ``KeepEqual`` and ``DropEqual`` actions. Regex capture groups are available.

        :schema: ProbeSpecTargetsIngressRelabelingConfigs
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f0d194a6ff04c922b2184244c79375666e994ec4de830d31f9ee5e68d5db00)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument modulus", value=modulus, expected_type=type_hints["modulus"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument replacement", value=replacement, expected_type=type_hints["replacement"])
            check_type(argname="argument separator", value=separator, expected_type=type_hints["separator"])
            check_type(argname="argument source_labels", value=source_labels, expected_type=type_hints["source_labels"])
            check_type(argname="argument target_label", value=target_label, expected_type=type_hints["target_label"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if modulus is not None:
            self._values["modulus"] = modulus
        if regex is not None:
            self._values["regex"] = regex
        if replacement is not None:
            self._values["replacement"] = replacement
        if separator is not None:
            self._values["separator"] = separator
        if source_labels is not None:
            self._values["source_labels"] = source_labels
        if target_label is not None:
            self._values["target_label"] = target_label

    @builtins.property
    def action(
        self,
    ) -> typing.Optional["ProbeSpecTargetsIngressRelabelingConfigsAction"]:
        '''action to perform based on the regex matching.

        ``Uppercase`` and ``Lowercase`` actions require Prometheus >= v2.36.0.
        ``DropEqual`` and ``KeepEqual`` actions require Prometheus >= v2.41.0.

        Default: "Replace"

        :schema: ProbeSpecTargetsIngressRelabelingConfigs#action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional["ProbeSpecTargetsIngressRelabelingConfigsAction"], result)

    @builtins.property
    def modulus(self) -> typing.Optional[jsii.Number]:
        '''modulus to take of the hash of the source label values.

        Only applicable when the action is ``HashMod``.

        :schema: ProbeSpecTargetsIngressRelabelingConfigs#modulus
        '''
        result = self._values.get("modulus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''regex defines the regular expression against which the extracted value is matched.

        :schema: ProbeSpecTargetsIngressRelabelingConfigs#regex
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replacement(self) -> typing.Optional[builtins.str]:
        '''replacement value against which a Replace action is performed if the regular expression matches.

        Regex capture groups are available.

        :schema: ProbeSpecTargetsIngressRelabelingConfigs#replacement
        '''
        result = self._values.get("replacement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def separator(self) -> typing.Optional[builtins.str]:
        '''separator defines the string between concatenated SourceLabels.

        :schema: ProbeSpecTargetsIngressRelabelingConfigs#separator
        '''
        result = self._values.get("separator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''sourceLabels defines the source labels select values from existing labels.

        Their content is
        concatenated using the configured Separator and matched against the
        configured regular expression.

        :schema: ProbeSpecTargetsIngressRelabelingConfigs#sourceLabels
        '''
        result = self._values.get("source_labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_label(self) -> typing.Optional[builtins.str]:
        '''targetLabel defines the label to which the resulting string is written in a replacement.

        It is mandatory for ``Replace``, ``HashMod``, ``Lowercase``, ``Uppercase``,
        ``KeepEqual`` and ``DropEqual`` actions.

        Regex capture groups are available.

        :schema: ProbeSpecTargetsIngressRelabelingConfigs#targetLabel
        '''
        result = self._values.get("target_label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecTargetsIngressRelabelingConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="comcoreosmonitoring.ProbeSpecTargetsIngressRelabelingConfigsAction"
)
class ProbeSpecTargetsIngressRelabelingConfigsAction(enum.Enum):
    '''action to perform based on the regex matching.

    ``Uppercase`` and ``Lowercase`` actions require Prometheus >= v2.36.0.
    ``DropEqual`` and ``KeepEqual`` actions require Prometheus >= v2.41.0.

    Default: "Replace"

    :schema: ProbeSpecTargetsIngressRelabelingConfigsAction
    '''

    REPLACE = "REPLACE"
    '''replace.'''
    KEEP = "KEEP"
    '''keep.'''
    DROP = "DROP"
    '''drop.'''
    HASHMOD = "HASHMOD"
    '''hashmod.'''
    LABELMAP = "LABELMAP"
    '''labelmap.'''
    LABELDROP = "LABELDROP"
    '''labeldrop.'''
    LABELKEEP = "LABELKEEP"
    '''labelkeep.'''
    LOWERCASE = "LOWERCASE"
    '''lowercase.'''
    UPPERCASE = "UPPERCASE"
    '''uppercase.'''
    KEEPEQUAL = "KEEPEQUAL"
    '''keepequal.'''
    DROPEQUAL = "DROPEQUAL"
    '''dropequal.'''


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecTargetsIngressSelector",
    jsii_struct_bases=[],
    name_mapping={
        "match_expressions": "matchExpressions",
        "match_labels": "matchLabels",
    },
)
class ProbeSpecTargetsIngressSelector:
    def __init__(
        self,
        *,
        match_expressions: typing.Optional[typing.Sequence[typing.Union["ProbeSpecTargetsIngressSelectorMatchExpressions", typing.Dict[builtins.str, typing.Any]]]] = None,
        match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''selector to select the Ingress objects.

        :param match_expressions: matchExpressions is a list of label selector requirements. The requirements are ANDed.
        :param match_labels: matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels map is equivalent to an element of matchExpressions, whose key field is "key", the operator is "In", and the values array contains only "value". The requirements are ANDed.

        :schema: ProbeSpecTargetsIngressSelector
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__824c697fb793291a8ee1f5e6cb70004a96f5cab540dcbeb2abe1a04aab187c6f)
            check_type(argname="argument match_expressions", value=match_expressions, expected_type=type_hints["match_expressions"])
            check_type(argname="argument match_labels", value=match_labels, expected_type=type_hints["match_labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if match_expressions is not None:
            self._values["match_expressions"] = match_expressions
        if match_labels is not None:
            self._values["match_labels"] = match_labels

    @builtins.property
    def match_expressions(
        self,
    ) -> typing.Optional[typing.List["ProbeSpecTargetsIngressSelectorMatchExpressions"]]:
        '''matchExpressions is a list of label selector requirements.

        The requirements are ANDed.

        :schema: ProbeSpecTargetsIngressSelector#matchExpressions
        '''
        result = self._values.get("match_expressions")
        return typing.cast(typing.Optional[typing.List["ProbeSpecTargetsIngressSelectorMatchExpressions"]], result)

    @builtins.property
    def match_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''matchLabels is a map of {key,value} pairs.

        A single {key,value} in the matchLabels
        map is equivalent to an element of matchExpressions, whose key field is "key", the
        operator is "In", and the values array contains only "value". The requirements are ANDed.

        :schema: ProbeSpecTargetsIngressSelector#matchLabels
        '''
        result = self._values.get("match_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecTargetsIngressSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecTargetsIngressSelectorMatchExpressions",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class ProbeSpecTargetsIngressSelectorMatchExpressions:
    def __init__(
        self,
        *,
        key: builtins.str,
        operator: builtins.str,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''A label selector requirement is a selector that contains values, a key, and an operator that relates the key and values.

        :param key: key is the label key that the selector applies to.
        :param operator: operator represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists and DoesNotExist.
        :param values: values is an array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. This array is replaced during a strategic merge patch.

        :schema: ProbeSpecTargetsIngressSelectorMatchExpressions
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bb211c32fed803933077d30221ae3997f5165b0b35c45fe0722cab2c615f9d4)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "operator": operator,
        }
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def key(self) -> builtins.str:
        '''key is the label key that the selector applies to.

        :schema: ProbeSpecTargetsIngressSelectorMatchExpressions#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''operator represents a key's relationship to a set of values.

        Valid operators are In, NotIn, Exists and DoesNotExist.

        :schema: ProbeSpecTargetsIngressSelectorMatchExpressions#operator
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''values is an array of string values.

        If the operator is In or NotIn,
        the values array must be non-empty. If the operator is Exists or DoesNotExist,
        the values array must be empty. This array is replaced during a strategic
        merge patch.

        :schema: ProbeSpecTargetsIngressSelectorMatchExpressions#values
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecTargetsIngressSelectorMatchExpressions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecTargetsStaticConfig",
    jsii_struct_bases=[],
    name_mapping={
        "labels": "labels",
        "relabeling_configs": "relabelingConfigs",
        "static": "static",
    },
)
class ProbeSpecTargetsStaticConfig:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        relabeling_configs: typing.Optional[typing.Sequence[typing.Union["ProbeSpecTargetsStaticConfigRelabelingConfigs", typing.Dict[builtins.str, typing.Any]]]] = None,
        static: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''staticConfig defines the static list of targets to probe and the relabeling configuration.

        If ``ingress`` is also defined, ``staticConfig`` takes precedence.
        More info: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#static_config.

        :param labels: labels defines all labels assigned to all metrics scraped from the targets.
        :param relabeling_configs: relabelingConfigs defines relabelings to be apply to the label set of the targets before it gets scraped. More info: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config
        :param static: static defines the list of hosts to probe.

        :schema: ProbeSpecTargetsStaticConfig
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed31334ed0d748aaae06f9b321f95e66bd6df365ed39735750b1c6292b6f1fe)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument relabeling_configs", value=relabeling_configs, expected_type=type_hints["relabeling_configs"])
            check_type(argname="argument static", value=static, expected_type=type_hints["static"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels
        if relabeling_configs is not None:
            self._values["relabeling_configs"] = relabeling_configs
        if static is not None:
            self._values["static"] = static

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''labels defines all labels assigned to all metrics scraped from the targets.

        :schema: ProbeSpecTargetsStaticConfig#labels
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def relabeling_configs(
        self,
    ) -> typing.Optional[typing.List["ProbeSpecTargetsStaticConfigRelabelingConfigs"]]:
        '''relabelingConfigs defines relabelings to be apply to the label set of the targets before it gets scraped.

        More info: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config

        :schema: ProbeSpecTargetsStaticConfig#relabelingConfigs
        '''
        result = self._values.get("relabeling_configs")
        return typing.cast(typing.Optional[typing.List["ProbeSpecTargetsStaticConfigRelabelingConfigs"]], result)

    @builtins.property
    def static(self) -> typing.Optional[typing.List[builtins.str]]:
        '''static defines the list of hosts to probe.

        :schema: ProbeSpecTargetsStaticConfig#static
        '''
        result = self._values.get("static")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecTargetsStaticConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecTargetsStaticConfigRelabelingConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "modulus": "modulus",
        "regex": "regex",
        "replacement": "replacement",
        "separator": "separator",
        "source_labels": "sourceLabels",
        "target_label": "targetLabel",
    },
)
class ProbeSpecTargetsStaticConfigRelabelingConfigs:
    def __init__(
        self,
        *,
        action: typing.Optional["ProbeSpecTargetsStaticConfigRelabelingConfigsAction"] = None,
        modulus: typing.Optional[jsii.Number] = None,
        regex: typing.Optional[builtins.str] = None,
        replacement: typing.Optional[builtins.str] = None,
        separator: typing.Optional[builtins.str] = None,
        source_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''RelabelConfig allows dynamic rewriting of the label set for targets, alerts, scraped samples and remote write samples.

        More info: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config

        :param action: action to perform based on the regex matching. ``Uppercase`` and ``Lowercase`` actions require Prometheus >= v2.36.0. ``DropEqual`` and ``KeepEqual`` actions require Prometheus >= v2.41.0. Default: "Replace"
        :param modulus: modulus to take of the hash of the source label values. Only applicable when the action is ``HashMod``.
        :param regex: regex defines the regular expression against which the extracted value is matched.
        :param replacement: replacement value against which a Replace action is performed if the regular expression matches. Regex capture groups are available.
        :param separator: separator defines the string between concatenated SourceLabels.
        :param source_labels: sourceLabels defines the source labels select values from existing labels. Their content is concatenated using the configured Separator and matched against the configured regular expression.
        :param target_label: targetLabel defines the label to which the resulting string is written in a replacement. It is mandatory for ``Replace``, ``HashMod``, ``Lowercase``, ``Uppercase``, ``KeepEqual`` and ``DropEqual`` actions. Regex capture groups are available.

        :schema: ProbeSpecTargetsStaticConfigRelabelingConfigs
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b71e6ad529e679c40f358958cee351501b9475c2ba5b44d648f909f2740e2516)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument modulus", value=modulus, expected_type=type_hints["modulus"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument replacement", value=replacement, expected_type=type_hints["replacement"])
            check_type(argname="argument separator", value=separator, expected_type=type_hints["separator"])
            check_type(argname="argument source_labels", value=source_labels, expected_type=type_hints["source_labels"])
            check_type(argname="argument target_label", value=target_label, expected_type=type_hints["target_label"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if modulus is not None:
            self._values["modulus"] = modulus
        if regex is not None:
            self._values["regex"] = regex
        if replacement is not None:
            self._values["replacement"] = replacement
        if separator is not None:
            self._values["separator"] = separator
        if source_labels is not None:
            self._values["source_labels"] = source_labels
        if target_label is not None:
            self._values["target_label"] = target_label

    @builtins.property
    def action(
        self,
    ) -> typing.Optional["ProbeSpecTargetsStaticConfigRelabelingConfigsAction"]:
        '''action to perform based on the regex matching.

        ``Uppercase`` and ``Lowercase`` actions require Prometheus >= v2.36.0.
        ``DropEqual`` and ``KeepEqual`` actions require Prometheus >= v2.41.0.

        Default: "Replace"

        :schema: ProbeSpecTargetsStaticConfigRelabelingConfigs#action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional["ProbeSpecTargetsStaticConfigRelabelingConfigsAction"], result)

    @builtins.property
    def modulus(self) -> typing.Optional[jsii.Number]:
        '''modulus to take of the hash of the source label values.

        Only applicable when the action is ``HashMod``.

        :schema: ProbeSpecTargetsStaticConfigRelabelingConfigs#modulus
        '''
        result = self._values.get("modulus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''regex defines the regular expression against which the extracted value is matched.

        :schema: ProbeSpecTargetsStaticConfigRelabelingConfigs#regex
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replacement(self) -> typing.Optional[builtins.str]:
        '''replacement value against which a Replace action is performed if the regular expression matches.

        Regex capture groups are available.

        :schema: ProbeSpecTargetsStaticConfigRelabelingConfigs#replacement
        '''
        result = self._values.get("replacement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def separator(self) -> typing.Optional[builtins.str]:
        '''separator defines the string between concatenated SourceLabels.

        :schema: ProbeSpecTargetsStaticConfigRelabelingConfigs#separator
        '''
        result = self._values.get("separator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''sourceLabels defines the source labels select values from existing labels.

        Their content is
        concatenated using the configured Separator and matched against the
        configured regular expression.

        :schema: ProbeSpecTargetsStaticConfigRelabelingConfigs#sourceLabels
        '''
        result = self._values.get("source_labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_label(self) -> typing.Optional[builtins.str]:
        '''targetLabel defines the label to which the resulting string is written in a replacement.

        It is mandatory for ``Replace``, ``HashMod``, ``Lowercase``, ``Uppercase``,
        ``KeepEqual`` and ``DropEqual`` actions.

        Regex capture groups are available.

        :schema: ProbeSpecTargetsStaticConfigRelabelingConfigs#targetLabel
        '''
        result = self._values.get("target_label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecTargetsStaticConfigRelabelingConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="comcoreosmonitoring.ProbeSpecTargetsStaticConfigRelabelingConfigsAction"
)
class ProbeSpecTargetsStaticConfigRelabelingConfigsAction(enum.Enum):
    '''action to perform based on the regex matching.

    ``Uppercase`` and ``Lowercase`` actions require Prometheus >= v2.36.0.
    ``DropEqual`` and ``KeepEqual`` actions require Prometheus >= v2.41.0.

    Default: "Replace"

    :schema: ProbeSpecTargetsStaticConfigRelabelingConfigsAction
    '''

    REPLACE = "REPLACE"
    '''replace.'''
    KEEP = "KEEP"
    '''keep.'''
    DROP = "DROP"
    '''drop.'''
    HASHMOD = "HASHMOD"
    '''hashmod.'''
    LABELMAP = "LABELMAP"
    '''labelmap.'''
    LABELDROP = "LABELDROP"
    '''labeldrop.'''
    LABELKEEP = "LABELKEEP"
    '''labelkeep.'''
    LOWERCASE = "LOWERCASE"
    '''lowercase.'''
    UPPERCASE = "UPPERCASE"
    '''uppercase.'''
    KEEPEQUAL = "KEEPEQUAL"
    '''keepequal.'''
    DROPEQUAL = "DROPEQUAL"
    '''dropequal.'''


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecTlsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "ca": "ca",
        "cert": "cert",
        "insecure_skip_verify": "insecureSkipVerify",
        "key_secret": "keySecret",
        "max_version": "maxVersion",
        "min_version": "minVersion",
        "server_name": "serverName",
    },
)
class ProbeSpecTlsConfig:
    def __init__(
        self,
        *,
        ca: typing.Optional[typing.Union["ProbeSpecTlsConfigCa", typing.Dict[builtins.str, typing.Any]]] = None,
        cert: typing.Optional[typing.Union["ProbeSpecTlsConfigCert", typing.Dict[builtins.str, typing.Any]]] = None,
        insecure_skip_verify: typing.Optional[builtins.bool] = None,
        key_secret: typing.Optional[typing.Union["ProbeSpecTlsConfigKeySecret", typing.Dict[builtins.str, typing.Any]]] = None,
        max_version: typing.Optional["ProbeSpecTlsConfigMaxVersion"] = None,
        min_version: typing.Optional["ProbeSpecTlsConfigMinVersion"] = None,
        server_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''tlsConfig defines the TLS configuration used by the client.

        :param ca: ca defines the Certificate authority used when verifying server certificates.
        :param cert: cert defines the Client certificate to present when doing client-authentication.
        :param insecure_skip_verify: insecureSkipVerify defines how to disable target certificate validation.
        :param key_secret: keySecret defines the Secret containing the client key file for the targets.
        :param max_version: maxVersion defines the maximum acceptable TLS version. It requires Prometheus >= v2.41.0 or Thanos >= v0.31.0.
        :param min_version: minVersion defines the minimum acceptable TLS version. It requires Prometheus >= v2.35.0 or Thanos >= v0.28.0.
        :param server_name: serverName is used to verify the hostname for the targets.

        :schema: ProbeSpecTlsConfig
        '''
        if isinstance(ca, dict):
            ca = ProbeSpecTlsConfigCa(**ca)
        if isinstance(cert, dict):
            cert = ProbeSpecTlsConfigCert(**cert)
        if isinstance(key_secret, dict):
            key_secret = ProbeSpecTlsConfigKeySecret(**key_secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f2f76cc98058d94d33ea95f52e743a0d00dbc0d25d136aed644660451a3646)
            check_type(argname="argument ca", value=ca, expected_type=type_hints["ca"])
            check_type(argname="argument cert", value=cert, expected_type=type_hints["cert"])
            check_type(argname="argument insecure_skip_verify", value=insecure_skip_verify, expected_type=type_hints["insecure_skip_verify"])
            check_type(argname="argument key_secret", value=key_secret, expected_type=type_hints["key_secret"])
            check_type(argname="argument max_version", value=max_version, expected_type=type_hints["max_version"])
            check_type(argname="argument min_version", value=min_version, expected_type=type_hints["min_version"])
            check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ca is not None:
            self._values["ca"] = ca
        if cert is not None:
            self._values["cert"] = cert
        if insecure_skip_verify is not None:
            self._values["insecure_skip_verify"] = insecure_skip_verify
        if key_secret is not None:
            self._values["key_secret"] = key_secret
        if max_version is not None:
            self._values["max_version"] = max_version
        if min_version is not None:
            self._values["min_version"] = min_version
        if server_name is not None:
            self._values["server_name"] = server_name

    @builtins.property
    def ca(self) -> typing.Optional["ProbeSpecTlsConfigCa"]:
        '''ca defines the Certificate authority used when verifying server certificates.

        :schema: ProbeSpecTlsConfig#ca
        '''
        result = self._values.get("ca")
        return typing.cast(typing.Optional["ProbeSpecTlsConfigCa"], result)

    @builtins.property
    def cert(self) -> typing.Optional["ProbeSpecTlsConfigCert"]:
        '''cert defines the Client certificate to present when doing client-authentication.

        :schema: ProbeSpecTlsConfig#cert
        '''
        result = self._values.get("cert")
        return typing.cast(typing.Optional["ProbeSpecTlsConfigCert"], result)

    @builtins.property
    def insecure_skip_verify(self) -> typing.Optional[builtins.bool]:
        '''insecureSkipVerify defines how to disable target certificate validation.

        :schema: ProbeSpecTlsConfig#insecureSkipVerify
        '''
        result = self._values.get("insecure_skip_verify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key_secret(self) -> typing.Optional["ProbeSpecTlsConfigKeySecret"]:
        '''keySecret defines the Secret containing the client key file for the targets.

        :schema: ProbeSpecTlsConfig#keySecret
        '''
        result = self._values.get("key_secret")
        return typing.cast(typing.Optional["ProbeSpecTlsConfigKeySecret"], result)

    @builtins.property
    def max_version(self) -> typing.Optional["ProbeSpecTlsConfigMaxVersion"]:
        '''maxVersion defines the maximum acceptable TLS version.

        It requires Prometheus >= v2.41.0 or Thanos >= v0.31.0.

        :schema: ProbeSpecTlsConfig#maxVersion
        '''
        result = self._values.get("max_version")
        return typing.cast(typing.Optional["ProbeSpecTlsConfigMaxVersion"], result)

    @builtins.property
    def min_version(self) -> typing.Optional["ProbeSpecTlsConfigMinVersion"]:
        '''minVersion defines the minimum acceptable TLS version.

        It requires Prometheus >= v2.35.0 or Thanos >= v0.28.0.

        :schema: ProbeSpecTlsConfig#minVersion
        '''
        result = self._values.get("min_version")
        return typing.cast(typing.Optional["ProbeSpecTlsConfigMinVersion"], result)

    @builtins.property
    def server_name(self) -> typing.Optional[builtins.str]:
        '''serverName is used to verify the hostname for the targets.

        :schema: ProbeSpecTlsConfig#serverName
        '''
        result = self._values.get("server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecTlsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecTlsConfigCa",
    jsii_struct_bases=[],
    name_mapping={"config_map": "configMap", "secret": "secret"},
)
class ProbeSpecTlsConfigCa:
    def __init__(
        self,
        *,
        config_map: typing.Optional[typing.Union["ProbeSpecTlsConfigCaConfigMap", typing.Dict[builtins.str, typing.Any]]] = None,
        secret: typing.Optional[typing.Union["ProbeSpecTlsConfigCaSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''ca defines the Certificate authority used when verifying server certificates.

        :param config_map: configMap defines the ConfigMap containing data to use for the targets.
        :param secret: secret defines the Secret containing data to use for the targets.

        :schema: ProbeSpecTlsConfigCa
        '''
        if isinstance(config_map, dict):
            config_map = ProbeSpecTlsConfigCaConfigMap(**config_map)
        if isinstance(secret, dict):
            secret = ProbeSpecTlsConfigCaSecret(**secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__234e2a343852f0f4e904cccc3cb1dec930b5f8176909a6ddb7481010aa74bd0b)
            check_type(argname="argument config_map", value=config_map, expected_type=type_hints["config_map"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config_map is not None:
            self._values["config_map"] = config_map
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def config_map(self) -> typing.Optional["ProbeSpecTlsConfigCaConfigMap"]:
        '''configMap defines the ConfigMap containing data to use for the targets.

        :schema: ProbeSpecTlsConfigCa#configMap
        '''
        result = self._values.get("config_map")
        return typing.cast(typing.Optional["ProbeSpecTlsConfigCaConfigMap"], result)

    @builtins.property
    def secret(self) -> typing.Optional["ProbeSpecTlsConfigCaSecret"]:
        '''secret defines the Secret containing data to use for the targets.

        :schema: ProbeSpecTlsConfigCa#secret
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional["ProbeSpecTlsConfigCaSecret"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecTlsConfigCa(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecTlsConfigCaConfigMap",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecTlsConfigCaConfigMap:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''configMap defines the ConfigMap containing data to use for the targets.

        :param key: The key to select.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the ConfigMap or its key must be defined.

        :schema: ProbeSpecTlsConfigCaConfigMap
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9341b8ca5893bbbc375ee845df167a5ef00337ea7ca1e6753f58bd413aa47e9c)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key to select.

        :schema: ProbeSpecTlsConfigCaConfigMap#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecTlsConfigCaConfigMap#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the ConfigMap or its key must be defined.

        :schema: ProbeSpecTlsConfigCaConfigMap#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecTlsConfigCaConfigMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecTlsConfigCaSecret",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecTlsConfigCaSecret:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''secret defines the Secret containing data to use for the targets.

        :param key: The key of the secret to select from. Must be a valid secret key.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecTlsConfigCaSecret
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b6e45532aef7bc005ec1829b394ed44b8f84c37256f4c22db7b4261e0003e39)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the secret to select from.

        Must be a valid secret key.

        :schema: ProbeSpecTlsConfigCaSecret#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecTlsConfigCaSecret#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecTlsConfigCaSecret#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecTlsConfigCaSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecTlsConfigCert",
    jsii_struct_bases=[],
    name_mapping={"config_map": "configMap", "secret": "secret"},
)
class ProbeSpecTlsConfigCert:
    def __init__(
        self,
        *,
        config_map: typing.Optional[typing.Union["ProbeSpecTlsConfigCertConfigMap", typing.Dict[builtins.str, typing.Any]]] = None,
        secret: typing.Optional[typing.Union["ProbeSpecTlsConfigCertSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''cert defines the Client certificate to present when doing client-authentication.

        :param config_map: configMap defines the ConfigMap containing data to use for the targets.
        :param secret: secret defines the Secret containing data to use for the targets.

        :schema: ProbeSpecTlsConfigCert
        '''
        if isinstance(config_map, dict):
            config_map = ProbeSpecTlsConfigCertConfigMap(**config_map)
        if isinstance(secret, dict):
            secret = ProbeSpecTlsConfigCertSecret(**secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4371ded8c915fa2c994afa358f8ac0bb1c0d7559e99e691e745d1460e43409f4)
            check_type(argname="argument config_map", value=config_map, expected_type=type_hints["config_map"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config_map is not None:
            self._values["config_map"] = config_map
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def config_map(self) -> typing.Optional["ProbeSpecTlsConfigCertConfigMap"]:
        '''configMap defines the ConfigMap containing data to use for the targets.

        :schema: ProbeSpecTlsConfigCert#configMap
        '''
        result = self._values.get("config_map")
        return typing.cast(typing.Optional["ProbeSpecTlsConfigCertConfigMap"], result)

    @builtins.property
    def secret(self) -> typing.Optional["ProbeSpecTlsConfigCertSecret"]:
        '''secret defines the Secret containing data to use for the targets.

        :schema: ProbeSpecTlsConfigCert#secret
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional["ProbeSpecTlsConfigCertSecret"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecTlsConfigCert(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecTlsConfigCertConfigMap",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecTlsConfigCertConfigMap:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''configMap defines the ConfigMap containing data to use for the targets.

        :param key: The key to select.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the ConfigMap or its key must be defined.

        :schema: ProbeSpecTlsConfigCertConfigMap
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8016cc953cc53b554483c2dddaacd44c835ba2b59aec482d7fed3d0a037180f7)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key to select.

        :schema: ProbeSpecTlsConfigCertConfigMap#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecTlsConfigCertConfigMap#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the ConfigMap or its key must be defined.

        :schema: ProbeSpecTlsConfigCertConfigMap#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecTlsConfigCertConfigMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecTlsConfigCertSecret",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecTlsConfigCertSecret:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''secret defines the Secret containing data to use for the targets.

        :param key: The key of the secret to select from. Must be a valid secret key.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecTlsConfigCertSecret
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef95113d17449f9e1eb740a0ed90d035b659431c2389555e793e28c32dbf63f4)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the secret to select from.

        Must be a valid secret key.

        :schema: ProbeSpecTlsConfigCertSecret#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecTlsConfigCertSecret#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecTlsConfigCertSecret#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecTlsConfigCertSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="comcoreosmonitoring.ProbeSpecTlsConfigKeySecret",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class ProbeSpecTlsConfigKeySecret:
    def __init__(
        self,
        *,
        key: builtins.str,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''keySecret defines the Secret containing the client key file for the targets.

        :param key: The key of the secret to select from. Must be a valid secret key.
        :param name: Name of the referent. This field is effectively required, but due to backwards compatibility is allowed to be empty. Instances of this type with an empty value here are almost certainly wrong. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
        :param optional: Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecTlsConfigKeySecret
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf8a4805fbee4c0395addcd1987dd45738bf0ed398a02a622b6de3ddb8bcaec)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the secret to select from.

        Must be a valid secret key.

        :schema: ProbeSpecTlsConfigKeySecret#key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent.

        This field is effectively required, but due to backwards compatibility is
        allowed to be empty. Instances of this type with an empty value here are
        almost certainly wrong.
        More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names

        :schema: ProbeSpecTlsConfigKeySecret#name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''Specify whether the Secret or its key must be defined.

        :schema: ProbeSpecTlsConfigKeySecret#optional
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeSpecTlsConfigKeySecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="comcoreosmonitoring.ProbeSpecTlsConfigMaxVersion")
class ProbeSpecTlsConfigMaxVersion(enum.Enum):
    '''maxVersion defines the maximum acceptable TLS version.

    It requires Prometheus >= v2.41.0 or Thanos >= v0.31.0.

    :schema: ProbeSpecTlsConfigMaxVersion
    '''

    TLS10 = "TLS10"
    '''TLS10.'''
    TLS11 = "TLS11"
    '''TLS11.'''
    TLS12 = "TLS12"
    '''TLS12.'''
    TLS13 = "TLS13"
    '''TLS13.'''


@jsii.enum(jsii_type="comcoreosmonitoring.ProbeSpecTlsConfigMinVersion")
class ProbeSpecTlsConfigMinVersion(enum.Enum):
    '''minVersion defines the minimum acceptable TLS version.

    It requires Prometheus >= v2.35.0 or Thanos >= v0.28.0.

    :schema: ProbeSpecTlsConfigMinVersion
    '''

    TLS10 = "TLS10"
    '''TLS10.'''
    TLS11 = "TLS11"
    '''TLS11.'''
    TLS12 = "TLS12"
    '''TLS12.'''
    TLS13 = "TLS13"
    '''TLS13.'''


__all__ = [
    "Probe",
    "ProbeProps",
    "ProbeSpec",
    "ProbeSpecAuthorization",
    "ProbeSpecAuthorizationCredentials",
    "ProbeSpecBasicAuth",
    "ProbeSpecBasicAuthPassword",
    "ProbeSpecBasicAuthUsername",
    "ProbeSpecBearerTokenSecret",
    "ProbeSpecFallbackScrapeProtocol",
    "ProbeSpecMetricRelabelings",
    "ProbeSpecMetricRelabelingsAction",
    "ProbeSpecNativeHistogramMinBucketFactor",
    "ProbeSpecOauth2",
    "ProbeSpecOauth2ClientId",
    "ProbeSpecOauth2ClientIdConfigMap",
    "ProbeSpecOauth2ClientIdSecret",
    "ProbeSpecOauth2ClientSecret",
    "ProbeSpecOauth2ProxyConnectHeader",
    "ProbeSpecOauth2TlsConfig",
    "ProbeSpecOauth2TlsConfigCa",
    "ProbeSpecOauth2TlsConfigCaConfigMap",
    "ProbeSpecOauth2TlsConfigCaSecret",
    "ProbeSpecOauth2TlsConfigCert",
    "ProbeSpecOauth2TlsConfigCertConfigMap",
    "ProbeSpecOauth2TlsConfigCertSecret",
    "ProbeSpecOauth2TlsConfigKeySecret",
    "ProbeSpecOauth2TlsConfigMaxVersion",
    "ProbeSpecOauth2TlsConfigMinVersion",
    "ProbeSpecParams",
    "ProbeSpecProber",
    "ProbeSpecProberProxyConnectHeader",
    "ProbeSpecProberScheme",
    "ProbeSpecScrapeProtocols",
    "ProbeSpecTargets",
    "ProbeSpecTargetsIngress",
    "ProbeSpecTargetsIngressNamespaceSelector",
    "ProbeSpecTargetsIngressRelabelingConfigs",
    "ProbeSpecTargetsIngressRelabelingConfigsAction",
    "ProbeSpecTargetsIngressSelector",
    "ProbeSpecTargetsIngressSelectorMatchExpressions",
    "ProbeSpecTargetsStaticConfig",
    "ProbeSpecTargetsStaticConfigRelabelingConfigs",
    "ProbeSpecTargetsStaticConfigRelabelingConfigsAction",
    "ProbeSpecTlsConfig",
    "ProbeSpecTlsConfigCa",
    "ProbeSpecTlsConfigCaConfigMap",
    "ProbeSpecTlsConfigCaSecret",
    "ProbeSpecTlsConfigCert",
    "ProbeSpecTlsConfigCertConfigMap",
    "ProbeSpecTlsConfigCertSecret",
    "ProbeSpecTlsConfigKeySecret",
    "ProbeSpecTlsConfigMaxVersion",
    "ProbeSpecTlsConfigMinVersion",
]

publication.publish()

def _typecheckingstub__d431973747a4e312d98bbfc6c85e22bfcc072205d8b977840cdd34994c446c3b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    spec: typing.Union[ProbeSpec, typing.Dict[builtins.str, typing.Any]],
    metadata: typing.Optional[typing.Union[_cdk8s_d3d9af27.ApiObjectMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dfdb1f8ee121f58da1f22691f2f6aa14bc10cbb8707eef9c91e85264c784a46(
    *,
    spec: typing.Union[ProbeSpec, typing.Dict[builtins.str, typing.Any]],
    metadata: typing.Optional[typing.Union[_cdk8s_d3d9af27.ApiObjectMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da9453333edbc627c631d6c0043f58d9dc9b96a470aabc5bda67f045c750a88(
    *,
    authorization: typing.Optional[typing.Union[ProbeSpecAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    basic_auth: typing.Optional[typing.Union[ProbeSpecBasicAuth, typing.Dict[builtins.str, typing.Any]]] = None,
    bearer_token_secret: typing.Optional[typing.Union[ProbeSpecBearerTokenSecret, typing.Dict[builtins.str, typing.Any]]] = None,
    convert_classic_histograms_to_nhcb: typing.Optional[builtins.bool] = None,
    enable_http2: typing.Optional[builtins.bool] = None,
    fallback_scrape_protocol: typing.Optional[ProbeSpecFallbackScrapeProtocol] = None,
    follow_redirects: typing.Optional[builtins.bool] = None,
    interval: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    keep_dropped_targets: typing.Optional[jsii.Number] = None,
    label_limit: typing.Optional[jsii.Number] = None,
    label_name_length_limit: typing.Optional[jsii.Number] = None,
    label_value_length_limit: typing.Optional[jsii.Number] = None,
    metric_relabelings: typing.Optional[typing.Sequence[typing.Union[ProbeSpecMetricRelabelings, typing.Dict[builtins.str, typing.Any]]]] = None,
    module: typing.Optional[builtins.str] = None,
    native_histogram_bucket_limit: typing.Optional[jsii.Number] = None,
    native_histogram_min_bucket_factor: typing.Optional[ProbeSpecNativeHistogramMinBucketFactor] = None,
    oauth2: typing.Optional[typing.Union[ProbeSpecOauth2, typing.Dict[builtins.str, typing.Any]]] = None,
    params: typing.Optional[typing.Sequence[typing.Union[ProbeSpecParams, typing.Dict[builtins.str, typing.Any]]]] = None,
    prober: typing.Optional[typing.Union[ProbeSpecProber, typing.Dict[builtins.str, typing.Any]]] = None,
    sample_limit: typing.Optional[jsii.Number] = None,
    scrape_class: typing.Optional[builtins.str] = None,
    scrape_classic_histograms: typing.Optional[builtins.bool] = None,
    scrape_protocols: typing.Optional[typing.Sequence[ProbeSpecScrapeProtocols]] = None,
    scrape_timeout: typing.Optional[builtins.str] = None,
    target_limit: typing.Optional[jsii.Number] = None,
    targets: typing.Optional[typing.Union[ProbeSpecTargets, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_config: typing.Optional[typing.Union[ProbeSpecTlsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53119ace9a7835b3dc700fa87720e6dd11a003f2a7fc4457715e90440952103f(
    *,
    credentials: typing.Optional[typing.Union[ProbeSpecAuthorizationCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517b59dcdc17adab6d92c779136e1af970c3610952d33993c1951b07b2b438c3(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4768e0bb103c7f5c864a395f4c7c73437a4bb218bd61f88ce14258902c233463(
    *,
    password: typing.Optional[typing.Union[ProbeSpecBasicAuthPassword, typing.Dict[builtins.str, typing.Any]]] = None,
    username: typing.Optional[typing.Union[ProbeSpecBasicAuthUsername, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__780ef3df5e7ff3c36cd640940223f69d3ed0f61e6cccb5a5fef1039879162e68(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e43c9454cc4ce860c775eb76aaf3e59407bfad140ff617ddc8b81d03f12957f(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a16eb69c2dbd20d71a7eeb9b0e7066b3f1c11e88f44ff60ef5064326b2fc6e89(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b7df01a5f3a31e8d2329909c14c55b34f6b76669ef783ab0f574f2a4fd436c(
    *,
    action: typing.Optional[ProbeSpecMetricRelabelingsAction] = None,
    modulus: typing.Optional[jsii.Number] = None,
    regex: typing.Optional[builtins.str] = None,
    replacement: typing.Optional[builtins.str] = None,
    separator: typing.Optional[builtins.str] = None,
    source_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b130555197feba1c2d7008bc599d472d9b7386f7b29b719e7f32340b972186(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d8c278e2bddb7a566817def41022cebbb7f0c4e1a3bbb9a2be8e89d44126c54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35546638facd27ef81d9c1565abe451319a91571a20f556580e86ba1d20429a2(
    *,
    client_id: typing.Union[ProbeSpecOauth2ClientId, typing.Dict[builtins.str, typing.Any]],
    client_secret: typing.Union[ProbeSpecOauth2ClientSecret, typing.Dict[builtins.str, typing.Any]],
    token_url: builtins.str,
    endpoint_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    no_proxy: typing.Optional[builtins.str] = None,
    proxy_connect_header: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[typing.Union[ProbeSpecOauth2ProxyConnectHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    proxy_from_environment: typing.Optional[builtins.bool] = None,
    proxy_url: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    tls_config: typing.Optional[typing.Union[ProbeSpecOauth2TlsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1be640787caefbccf5bf6ea2c41346de4deaa3542fa016ffcd1ad2f7b03947(
    *,
    config_map: typing.Optional[typing.Union[ProbeSpecOauth2ClientIdConfigMap, typing.Dict[builtins.str, typing.Any]]] = None,
    secret: typing.Optional[typing.Union[ProbeSpecOauth2ClientIdSecret, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b58566d2cc8954a47735bf7be6b762a394014c89472a4e9a617944a055f9eba(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3883f2226aad7334fc8c12f1bd7a408a3265db413dbe8a1e3d4a338d6977eb5(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4814e43f5970f5d96976d6e9d6055b8a3423197f1bd40f0b4cc46f6dec7d51(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15168185ff890e76ebda9406137eb68adc01cdc9c5aab9c30a2c5826a7006e00(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acab03ee682702fd6d01e755686c70644b8c90eb20338257444d40971a8fa5e5(
    *,
    ca: typing.Optional[typing.Union[ProbeSpecOauth2TlsConfigCa, typing.Dict[builtins.str, typing.Any]]] = None,
    cert: typing.Optional[typing.Union[ProbeSpecOauth2TlsConfigCert, typing.Dict[builtins.str, typing.Any]]] = None,
    insecure_skip_verify: typing.Optional[builtins.bool] = None,
    key_secret: typing.Optional[typing.Union[ProbeSpecOauth2TlsConfigKeySecret, typing.Dict[builtins.str, typing.Any]]] = None,
    max_version: typing.Optional[ProbeSpecOauth2TlsConfigMaxVersion] = None,
    min_version: typing.Optional[ProbeSpecOauth2TlsConfigMinVersion] = None,
    server_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b9fbb23975748c32531df12669a8d0336e3f150fe8dfc6d0523b7872181e9db(
    *,
    config_map: typing.Optional[typing.Union[ProbeSpecOauth2TlsConfigCaConfigMap, typing.Dict[builtins.str, typing.Any]]] = None,
    secret: typing.Optional[typing.Union[ProbeSpecOauth2TlsConfigCaSecret, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb44bff72110d97ac3438464c8c567658490b004d26407730c443ccc51b13493(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ebb235751ba9f0be493e52ef41f277eeec2f4f835eee9624496ef01c19958b5(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa77d74aa81f6f522990bdc835c51cbbacfbaaf72af7fa1e3fc03fca7a149e0d(
    *,
    config_map: typing.Optional[typing.Union[ProbeSpecOauth2TlsConfigCertConfigMap, typing.Dict[builtins.str, typing.Any]]] = None,
    secret: typing.Optional[typing.Union[ProbeSpecOauth2TlsConfigCertSecret, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf145604647ba536a0b9fb2de88a38dc6edc7f9a5b0f218814bad74a25fedf7(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1ee302452088816f5aa0ff7b10ed5e5fb4982d155b44ac8bbf2bf6b86f4790(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33dc52b7c1489b1ef2cb0651104939ff50b5f5fc1d5e6875fce37f06ffe66295(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83e6f1b9e7885581ddfaea5d163a9a2c94860c9d3f775f17b2f2191928513d2(
    *,
    name: builtins.str,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6684cb5ff968185a87d2fade885ee91d9329d7babe8bc8fbb69c24e63cd7cdb7(
    *,
    url: builtins.str,
    no_proxy: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    proxy_connect_header: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[typing.Union[ProbeSpecProberProxyConnectHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    proxy_from_environment: typing.Optional[builtins.bool] = None,
    proxy_url: typing.Optional[builtins.str] = None,
    scheme: typing.Optional[ProbeSpecProberScheme] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735075c33de8beaf61a817a03a8a9ef456504a89e716a6b517da4fee912fe297(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3c2540b1ee2c4ddde6e123dcd197b358060a8869e20cd6c41672ed67f10a20(
    *,
    ingress: typing.Optional[typing.Union[ProbeSpecTargetsIngress, typing.Dict[builtins.str, typing.Any]]] = None,
    static_config: typing.Optional[typing.Union[ProbeSpecTargetsStaticConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557d9655fcc58a0dbbcd62cd19e97562f13c2ffcfe419b3f3753a95f63268155(
    *,
    namespace_selector: typing.Optional[typing.Union[ProbeSpecTargetsIngressNamespaceSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    relabeling_configs: typing.Optional[typing.Sequence[typing.Union[ProbeSpecTargetsIngressRelabelingConfigs, typing.Dict[builtins.str, typing.Any]]]] = None,
    selector: typing.Optional[typing.Union[ProbeSpecTargetsIngressSelector, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ddf059c2fe1e2ea0fa1c287113225d84e1ecfb842e8fc2e3de29f020d957f78(
    *,
    any: typing.Optional[builtins.bool] = None,
    match_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f0d194a6ff04c922b2184244c79375666e994ec4de830d31f9ee5e68d5db00(
    *,
    action: typing.Optional[ProbeSpecTargetsIngressRelabelingConfigsAction] = None,
    modulus: typing.Optional[jsii.Number] = None,
    regex: typing.Optional[builtins.str] = None,
    replacement: typing.Optional[builtins.str] = None,
    separator: typing.Optional[builtins.str] = None,
    source_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824c697fb793291a8ee1f5e6cb70004a96f5cab540dcbeb2abe1a04aab187c6f(
    *,
    match_expressions: typing.Optional[typing.Sequence[typing.Union[ProbeSpecTargetsIngressSelectorMatchExpressions, typing.Dict[builtins.str, typing.Any]]]] = None,
    match_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb211c32fed803933077d30221ae3997f5165b0b35c45fe0722cab2c615f9d4(
    *,
    key: builtins.str,
    operator: builtins.str,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed31334ed0d748aaae06f9b321f95e66bd6df365ed39735750b1c6292b6f1fe(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    relabeling_configs: typing.Optional[typing.Sequence[typing.Union[ProbeSpecTargetsStaticConfigRelabelingConfigs, typing.Dict[builtins.str, typing.Any]]]] = None,
    static: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b71e6ad529e679c40f358958cee351501b9475c2ba5b44d648f909f2740e2516(
    *,
    action: typing.Optional[ProbeSpecTargetsStaticConfigRelabelingConfigsAction] = None,
    modulus: typing.Optional[jsii.Number] = None,
    regex: typing.Optional[builtins.str] = None,
    replacement: typing.Optional[builtins.str] = None,
    separator: typing.Optional[builtins.str] = None,
    source_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f2f76cc98058d94d33ea95f52e743a0d00dbc0d25d136aed644660451a3646(
    *,
    ca: typing.Optional[typing.Union[ProbeSpecTlsConfigCa, typing.Dict[builtins.str, typing.Any]]] = None,
    cert: typing.Optional[typing.Union[ProbeSpecTlsConfigCert, typing.Dict[builtins.str, typing.Any]]] = None,
    insecure_skip_verify: typing.Optional[builtins.bool] = None,
    key_secret: typing.Optional[typing.Union[ProbeSpecTlsConfigKeySecret, typing.Dict[builtins.str, typing.Any]]] = None,
    max_version: typing.Optional[ProbeSpecTlsConfigMaxVersion] = None,
    min_version: typing.Optional[ProbeSpecTlsConfigMinVersion] = None,
    server_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234e2a343852f0f4e904cccc3cb1dec930b5f8176909a6ddb7481010aa74bd0b(
    *,
    config_map: typing.Optional[typing.Union[ProbeSpecTlsConfigCaConfigMap, typing.Dict[builtins.str, typing.Any]]] = None,
    secret: typing.Optional[typing.Union[ProbeSpecTlsConfigCaSecret, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9341b8ca5893bbbc375ee845df167a5ef00337ea7ca1e6753f58bd413aa47e9c(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6e45532aef7bc005ec1829b394ed44b8f84c37256f4c22db7b4261e0003e39(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4371ded8c915fa2c994afa358f8ac0bb1c0d7559e99e691e745d1460e43409f4(
    *,
    config_map: typing.Optional[typing.Union[ProbeSpecTlsConfigCertConfigMap, typing.Dict[builtins.str, typing.Any]]] = None,
    secret: typing.Optional[typing.Union[ProbeSpecTlsConfigCertSecret, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8016cc953cc53b554483c2dddaacd44c835ba2b59aec482d7fed3d0a037180f7(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef95113d17449f9e1eb740a0ed90d035b659431c2389555e793e28c32dbf63f4(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf8a4805fbee4c0395addcd1987dd45738bf0ed398a02a622b6de3ddb8bcaec(
    *,
    key: builtins.str,
    name: typing.Optional[builtins.str] = None,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
